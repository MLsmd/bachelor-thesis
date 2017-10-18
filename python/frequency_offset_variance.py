#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy as np
from gnuradio import gr
from gnuradio import blocks
from gnuradio import analog
import math
import dab
import dab_research

'''
Messung der Varianz des Frequenzoffsets bei verschiedenen SNR Szenarien
'''

class measure_freq_offset(gr.top_block):
    def __init__(self, SNR):
        gr.top_block.__init__(self)

        #data_source = blocks.vector_source_c_make(rx)
        data_source = blocks.file_source_make(gr.sizeof_gr_complex, "171011_recorded_iq_data.dat")
        noise_amplitude = 10**((-38.0-SNR)/20.0)
        #print "noise ampl: " + str(noise_amplitude)
        noise_source = analog.noise_source_c_make(analog.GR_GAUSSIAN, noise_amplitude)
        add = blocks.add_cc_make()
        measure = dab_research.measure_freq_offset_cf_make()
        head = blocks.head_make(gr.sizeof_float, 1000)
        sink = blocks.vector_sink_f_make()
        self.connect(data_source, add, measure, head, sink)
        self.connect(noise_source, (add, 1))
        self.run()
        self.sink_data = sink.data()
        #print self.sink_data
        self.data = np.asarray(self.sink_data)

# SNR vector
noise_range = np.asarray((0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0))
freq_var = np.zeros(len(noise_range))
freq_std = np.zeros(len(noise_range))
# calculate frequency offset for each SNR
i = 0
for SNR in noise_range:
    flowgraph = measure_freq_offset(SNR)
    f_offset = flowgraph.data
    # convert to Hz
    f_offset = np.multiply(np.absolute(f_offset), 1000.0/(2.0*np.pi))
    # calculate variance and std
    freq_var[i] = np.var(f_offset)
    freq_std[i] = np.std(f_offset)
    i += 1

print freq_std
print freq_var
