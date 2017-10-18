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


#ifndef INCLUDED_DAB_RESEARCH_MEASURE_FREQ_OFFSET_CF_H
#define INCLUDED_DAB_RESEARCH_MEASURE_FREQ_OFFSET_CF_H

#include <dab_research/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace dab_research {

    /*!
     * \brief <+description of block+>
     * \ingroup dab_research
     *
     */
    class DAB_RESEARCH_API measure_freq_offset_cf : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<measure_freq_offset_cf> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of dab_research::measure_freq_offset_cf.
       *
       * To avoid accidental use of raw pointers, dab_research::measure_freq_offset_cf's
       * constructor is in a private implementation
       * class. dab_research::measure_freq_offset_cf::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace dab_research
} // namespace gr

#endif /* INCLUDED_DAB_RESEARCH_MEASURE_FREQ_OFFSET_CF_H */

