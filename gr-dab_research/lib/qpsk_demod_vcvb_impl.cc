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
#include "qpsk_demod_vcvb_impl.h"

namespace gr {
  namespace dab_research {

    qpsk_demod_vcvb::sptr
    qpsk_demod_vcvb::make()
    {
      return gnuradio::get_initial_sptr
        (new qpsk_demod_vcvb_impl());
    }

    /*
     * The private constructor
     */
    qpsk_demod_vcvb_impl::qpsk_demod_vcvb_impl()
      : gr::sync_block("qpsk_demod_vcvb",
              gr::io_signature::make(1, 1, 1536 * sizeof(gr_complex)),
              gr::io_signature::make(1, 1, 3072 * sizeof(char)))
    {
      d_symbol_length = 1536;
    }

    /*
     * Our virtual destructor.
     */
    qpsk_demod_vcvb_impl::~qpsk_demod_vcvb_impl()
    {
    }

    int
    qpsk_demod_vcvb_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      char *out = (char *) output_items[0];

      for (int i = 0; i < noutput_items; ++i) {
        for (int j = 0; j < 1536; ++j) {
          if(in[i*d_symbol_length + j].real() < 0){
            out[i*2*d_symbol_length + j] = 0x01;
          }
          else{
            out[i*2*d_symbol_length + j] = 0x00;
          }
          if(in[i*d_symbol_length + j].imag() < 0){
            out[(i*2+1)*d_symbol_length + j] = 0x01;
          }
          else{
            out[(i*2+1)*d_symbol_length + j] = 0x00;
          }
        }
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace dab_research */
} /* namespace gr */

