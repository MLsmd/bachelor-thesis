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
#include "measure_fib_error_rate_impl.h"
#include "crc16.h"
#include "FIC.h"

namespace gr {
  namespace dab_research {

    measure_fib_error_rate::sptr
    measure_fib_error_rate::make()
    {
      return gnuradio::get_initial_sptr
        (new measure_fib_error_rate_impl());
    }

    /*
     * The private constructor
     */
    measure_fib_error_rate_impl::measure_fib_error_rate_impl()
      : gr::sync_block("measure_fib_error_rate",
              gr::io_signature::make(1, 1, sizeof(char)*32),
              gr::io_signature::make(2, 2, sizeof(char)))
    {}

    /*
     * Our virtual destructor.
     */
    measure_fib_error_rate_impl::~measure_fib_error_rate_impl()
    {
    }

    int
    measure_fib_error_rate_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const char *in = (const char *) input_items[0];
      char *out_ok = (char *) output_items[0];
      char *out_fail = (char *) output_items[1];

      for (int i = 0; i < noutput_items; ++i) {
        if (crc16(in, FIB_LENGTH, FIB_CRC_POLY, FIB_CRC_INITSTATE) != 0){
          out_ok[i] = 0;
          out_fail[i] = 1;
        }
        else{
          out_ok[i] = 1;
          out_fail[i] = 0;
        }
        in += 32;
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace dab_research */
} /* namespace gr */

