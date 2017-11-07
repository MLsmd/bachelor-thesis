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
import dab
import dab_research

iterations = 1000

'''
measure the rate of passed and failed firecodes
'''

class loopback(gr.top_block):
    def __init__(self, power, SNR, protection, address, size):
        gr.top_block.__init__(self)
        dp = dab.parameters.dab_parameters(mode=1, sample_rate=2048000, verbose=False)

        data_source = blocks.file_source_make(gr.sizeof_gr_complex, "data/gen_iq_A1_A3.dat", False)
        noise_amplitude = 10 ** ((power - SNR) / 20.0)
        noise_source = analog.noise_source_c_make(analog.GR_GAUSSIAN, noise_amplitude)
        add = blocks.add_cc_make()
        demod = dab.ofdm_demod_cc(dp)
        msc_decode = dab.msc_decode(dp, address, size, protection)
        fic_null = blocks.null_sink_make(gr.sizeof_gr_complex*1536)
        s2v_fire = blocks.stream_to_vector_make(gr.sizeof_char, 336)
        firecode = dab_research.firecode_check_bb_make(14)
        head_iq = blocks.head_make(gr.sizeof_gr_complex, iterations * 49152)
        head1 = blocks.head_make(gr.sizeof_char, iterations+15)
        head2 = blocks.head_make(gr.sizeof_char, iterations*24*112)
        ok_sink = blocks.vector_sink_b_make()

        self.connect(data_source, add, demod, fic_null)
        self.connect((demod, 1), msc_decode, firecode, head1, ok_sink)
        self.connect(noise_source, (add, 1))
        self.run()
        self.ok_data = np.asarray(ok_sink.data())

# measure power of iq_data
iq_gen = np.fromfile('data/gen_iq_A1_A3.dat', dtype=np.complex64, count=30720000)
power = 10 * np.log10(np.mean(np.square(np.absolute(iq_gen))))
print "measured power = " + str(power)


# A1
noise_range = np.arange(4.0, 6.0, 1.0)
successes = np.zeros(len(noise_range))
real_iterations = np.zeros(len(noise_range))
# calculate FIC error rate
for i,SNR in enumerate(noise_range):
    print "Simulating A1 SNR " + str(SNR)
    flowgraph = loopback(power, SNR, 0, 0, 168)
    # calculate variance and std
    successes[i] = np.count_nonzero(flowgraph.ok_data[15:])
    real_iterations[i] = len(flowgraph.ok_data) - 15
    print "real iterations: " + str(real_iterations[i])
    print "successes: " + str(successes[i])

print "final results A1: " + str(np.divide(np.subtract(real_iterations, successes),real_iterations))
np.savetxt("results/AWGN_Firecode_A1.dat", np.c_[noise_range, np.divide(np.subtract(real_iterations, successes),real_iterations)], delimiter=' ')

