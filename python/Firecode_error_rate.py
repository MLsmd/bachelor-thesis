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

iterations = 1000

'''
measure the rate of passed and failed firecodes
'''

class loopback(gr.top_block):
    def __init__(self, power, SNR):
        gr.top_block.__init__(self)
        dp = dab.parameters.dab_parameters(mode=1, sample_rate=2048000, verbose=False)

        data_source = blocks.file_source_make(gr.sizeof_gr_complex, "data/pure_dab_long.dat")
        noise_amplitude = 10 ** ((power - SNR) / 20.0)
        noise_source = analog.noise_source_c_make(analog.GR_GAUSSIAN, noise_amplitude)
        add = blocks.add_cc_make()
        demod = dab.ofdm_demod_cc(dp)
        msc_decode = dab.msc_decode(dp, 0, 84, 2)
        fic_null = blocks.null_sink_make(gr.sizeof_gr_complex*1536)
        s2v_fire = blocks.stream_to_vector_make(gr.sizeof_char, 336)
        firecode = dab_research.firecode_check_bb_make(14)
        head_iq = blocks.head_make(gr.sizeof_gr_complex, iterations * 49152)
        head1 = blocks.head_make(gr.sizeof_char, iterations)
        head2 = blocks.head_make(gr.sizeof_char, iterations*24*112)
        ok_sink = blocks.vector_sink_b_make()

        self.connect(data_source, add, demod, fic_null)
        self.connect((demod, 1), msc_decode, head2, firecode, head1, ok_sink)
        self.connect(noise_source, (add, 1))
        self.run()
        self.ok_data = np.asarray(ok_sink.data())



#
# # SNR vector
# noise_range = np.asarray((10.0, 20.0))
# successes = np.zeros(len(noise_range)*4)
# # calculate FIC error rate
# i = 0
# for SNR in noise_range:
#     for j in range(0,1):
#         flowgraph = loopback(power, SNR, 2)
#         # calculate variance and std
#         successes[i] = np.count_nonzero(flowgraph.ok_data)
#         i += 1
#
# print "fail rate: " + str((iterations-successes)/iterations)

#np.savetxt("results/.dat", np.c_[noise_range, (iterations-successes)/iterations], delimiter=' ')
flowgraph = loopback(-34.0, 20)
print flowgraph.ok_data