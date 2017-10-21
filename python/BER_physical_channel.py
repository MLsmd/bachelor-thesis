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
Messung der BER des physical channels
'''

class loopback(gr.top_block):
    def __init__(self, data, SNR):
        gr.top_block.__init__(self)
        dp = dab.parameters.dab_parameters(mode=1, sample_rate=2048000, verbose=False)

        # random but known bit data as source
        data_source = blocks.vector_source_b(data, True)
        pack = blocks.unpacked_to_packed_bb_make(1, gr.GR_MSB_FIRST)
        s2v = blocks.stream_to_vector_make(gr.sizeof_char, 384)
        trigsrc = blocks.vector_source_b([1] + [0] * (dp.symbols_per_frame - 2), True)

        # ofdm mod
        mod = dab.ofdm_mod(dp)

        # noise source
        noise_amplitude = 10**((-34.4220877-SNR)/20.0)
        noise_source = analog.noise_source_c_make(analog.GR_GAUSSIAN, noise_amplitude)

        # add noise to ofdm signal
        add = blocks.add_cc_make()

        # demodulate noisy signal
        demod = dab.ofdm_demod_cc(dp)
        qpsk = dab_research.qpsk_demod_vcvb_make()
        v2s_qpsk = blocks.vector_to_stream_make(gr.sizeof_char, 3072)

        # data sinks
        fic_sink = blocks.vector_sink_b_make()
        null_sink = blocks.null_sink_make(gr.sizeof_gr_complex*1536)

        head = blocks.head_make(gr.sizeof_char, 100)

        # connect everything
        self.connect(data_source, pack, s2v, mod, add, demod, null_sink)
        self.connect((demod, 1), qpsk, v2s_qpsk, head, fic_sink)
        self.connect(noise_source, (add, 1))
        self.connect(trigsrc, (mod, 1))
        self.run()
        self.sink_data = fic_sink.data()
        self.data = np.asarray(self.sink_data)
        print "sink bits: " + str(self.data)



# SNR vector
noise_range = np.asarray((0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0))
# calculate frequency offset for each SNR
#i = 0
# for SNR in noise_range:
#     flowgraph = measure_freq_offset(power, SNR)
#     f_offset = flowgraph.data
#     # convert to Hz
#     f_offset = np.multiply(np.absolute(f_offset), 1000.0/(2.0*np.pi))
#     # calculate variance and std
#     freq_var[i] = np.var(f_offset)
#     freq_std[i] = np.std(f_offset)
#     i += 1

source_bits = np.random.randint(2, size=1000000)
print "source bits: " + str(source_bits[0:100])
flowgraph = loopback(source_bits, 20)

#np.savetxt("results/frequency_offset_variance.dat", np.c_[noise_range, freq_var], delimiter=' ')
