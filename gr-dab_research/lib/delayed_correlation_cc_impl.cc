/* -*- c++ -*- */
/* 
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "delayed_correlation_cc_impl.h"

namespace gr {
  namespace dab_research {

    delayed_correlation_cc::sptr
    delayed_correlation_cc::make()
    {
      return gnuradio::get_initial_sptr
        (new delayed_correlation_cc_impl());
    }

    /*
     * The private constructor
     */
    delayed_correlation_cc_impl::delayed_correlation_cc_impl()
      : gr::block("delayed_correlation_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
      d_correlation = 0;
      d_energy_prefix = 1;
      d_energy_repetition = 1;
      d_NULL_symbol_energy = 1;
      d_frequency_offset = 0;
      d_NULL_detected = false;
      d_moving_average_counter = 0;
      d_frame_count = 1;
      d_frame_length_count = 0;
      d_wait_for_NULL = true;
      d_on_triangle = false;
      d_acquisition = false;
    }

    /*
     * Our virtual destructor.
     */
    delayed_correlation_cc_impl::~delayed_correlation_cc_impl()
    {
    }

    void
    delayed_correlation_cc_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items;
    }

    bool
    delayed_correlation_cc_impl::detect_start_of_symbol()
    {
      if(d_on_triangle){
        if(d_correlation_normalized_magnitude < 0.5){
          // we left the triangle
          d_on_triangle = false;
          return false;
        }
        else{
          // we are still on the triangle but we already picked our pre-peak value
          return false;
        }
      }
      else{
        // not on a correlation triangle yet
        if(d_correlation_normalized_magnitude > 0.85){
          // no we are on the triangle
          d_on_triangle = true;
          return true;
        }
        else{
          // no triangle here
          return false;
        }
      }
    }

    void
    delayed_correlation_cc_impl::delayed_correlation(const gr_complex *sample, bool new_calculation)
    {
      if (d_moving_average_counter > 100000 || d_moving_average_counter == 0 || new_calculation) {
        if (d_moving_average_counter == 0 && (!new_calculation)) {
          // first value is calculated completely, next values are calculated with moving average
          d_moving_average_counter++;
        } else {
          // reset counter
          d_moving_average_counter = 0;
        }
        // calculate delayed correlation for this sample completely
        d_correlation = 0;
        for (int j = 0; j < d_cyclic_prefix_length; j++) {
          d_correlation += sample[j] * conj(sample[d_symbol_length + j]);
        }
        // calculate energy of cyclic prefix for this sample completely
        d_energy_prefix = 0;
        for (int j = 0; j < d_cyclic_prefix_length; j++) {
          d_energy_prefix += std::real(sample[j] * conj(sample[j]));
        }
        // calculate energy of its repetition for this sample completely
        d_energy_repetition = 0;
        for (int j = 0; j < d_cyclic_prefix_length; j++) {
          d_energy_repetition += std::real(sample[j + d_symbol_length] * conj(sample[j + d_symbol_length]));
        }
      } else {
        // calculate next step for moving average
        d_correlation +=
                sample[d_cyclic_prefix_length - 1] * conj(sample[d_symbol_length + d_cyclic_prefix_length - 1]);
        d_energy_prefix += std::real(sample[d_cyclic_prefix_length - 1] * conj(sample[d_cyclic_prefix_length - 1]));
        d_energy_repetition += std::real(sample[d_symbol_length + d_cyclic_prefix_length - 1] *
                                         conj(sample[d_symbol_length + d_cyclic_prefix_length - 1]));
        d_correlation -= sample[0] * conj(sample[d_symbol_length]);
        d_energy_prefix -= std::real(sample[0] * conj(sample[0]));
        d_energy_repetition -= std::real(sample[d_symbol_length] * conj(sample[d_symbol_length]));
        d_moving_average_counter++;
      }
      // normalize
      d_correlation_normalized = d_correlation / std::sqrt(d_energy_prefix * d_energy_repetition);
      // calculate magnitude
      d_correlation_normalized_magnitude = d_correlation_normalized.real() * d_correlation_normalized.real() +
                                           d_correlation_normalized.imag() * d_correlation_normalized.imag();
    }

    int
    delayed_correlation_cc_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];

      for (int i = 0; i < noutput_items - d_cyclic_prefix_length - d_symbol_length; ++i) {
        delayed_correlation(&in[i], false);
        out[i] = d_correlation_normalized;
        if(detect_start_of_symbol()){
          if (d_NULL_detected && (d_energy_prefix > d_NULL_symbol_energy * 2)) {
            add_item_tag(0, nitems_written(0) + i, pmt::mp("Start of Frame"),
                         pmt::from_float(std::arg(d_correlation)));
            d_NULL_detected = false;
          }
        }
        else {
          if (((!d_NULL_detected) && (d_energy_prefix / d_energy_repetition < 0.1))) {
            // NULL symbol detection, if energy is < 0.1 * energy a symbol time later
            d_NULL_symbol_energy = d_energy_prefix;
            d_NULL_detected = true;
          }
        }
      }
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (noutput_items - d_cyclic_prefix_length - d_symbol_length);

      // Tell runtime system how many output items we produced.
      return noutput_items - d_cyclic_prefix_length - d_symbol_length;
    }

  } /* namespace dab_research */
} /* namespace gr */

