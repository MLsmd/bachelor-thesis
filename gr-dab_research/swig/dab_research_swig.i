/* -*- c++ -*- */

#define DAB_RESEARCH_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "dab_research_swig_doc.i"

%{
#include "dab_research/delayed_correlation_cc.h"
#include "dab_research/measure_freq_offset_cf.h"
%}


%include "dab_research/delayed_correlation_cc.h"
GR_SWIG_BLOCK_MAGIC2(dab_research, delayed_correlation_cc);
%include "dab_research/measure_freq_offset_cf.h"
GR_SWIG_BLOCK_MAGIC2(dab_research, measure_freq_offset_cf);