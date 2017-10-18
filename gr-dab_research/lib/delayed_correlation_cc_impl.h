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

#ifndef INCLUDED_DAB_RESEARCH_DELAYED_CORRELATION_CC_IMPL_H
#define INCLUDED_DAB_RESEARCH_DELAYED_CORRELATION_CC_IMPL_H

#include <dab_research/delayed_correlation_cc.h>

namespace gr {
  namespace dab_research {

    class delayed_correlation_cc_impl : public delayed_correlation_cc
    {
     private:
      int d_symbol_length = 2048;
      int d_cyclic_prefix_length = 504;
      int d_moving_average_counter;
      gr_complex d_correlation;
      gr_complex d_correlation_normalized;
      float d_correlation_normalized_magnitude;
      float d_correlation_normalized_phase;
      float d_energy_prefix;
      float d_energy_repetition;
      float d_NULL_symbol_energy;
      float d_frequency_offset;
      bool d_NULL_detected;
      int d_frame_count;
      int d_frame_length_count;
      bool d_wait_for_NULL;
      bool d_on_triangle;
      bool d_acquisition;

      int d_nwritten;

     public:
      delayed_correlation_cc_impl();
      ~delayed_correlation_cc_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      void delayed_correlation(const gr_complex *sample, bool new_calculation);
      bool detect_start_of_symbol();

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace dab_research
} // namespace gr

#endif /* INCLUDED_DAB_RESEARCH_DELAYED_CORRELATION_CC_IMPL_H */

