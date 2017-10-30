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
import matplotlib.pyplot as plt
from gnuradio import gr
from gnuradio import blocks
from gnuradio import analog
from gnuradio import filter
from gnuradio import channels
import LTE_models
import math
import dab
import dab_research

'''
Messung der BER des physical channels
'''

class loopback(gr.top_block):
    def __init__(self, SNR, taps, type):
        gr.top_block.__init__(self)
        dp = dab.parameters.dab_parameters(mode=1, sample_rate=2048000, verbose=False)

        # random but known bit data as source
        data_source = analog.random_uniform_source_b_make(0, 256, 0)
        unpack_ref = blocks.packed_to_unpacked_bb_make(1, gr.GR_MSB_FIRST)
        ref_data_sink = blocks.vector_sink_b_make()
        s2v = blocks.stream_to_vector_make(gr.sizeof_char, 384)
        trigsrc = blocks.vector_source_b([1] + [0] * (dp.symbols_per_frame - 2), True)

        # ofdm mod
        mod = dab.ofdm_mod(dp)

        # noise source
        noise_amplitude = 10**((-34.4220877-SNR)/20.0)
        noise_source = analog.noise_source_c_make(analog.GR_GAUSSIAN, noise_amplitude)

        # channel model
        if type == "AWGN":
            channel = channels.channel_model_make(noise_voltage=noise_amplitude, frequency_offset=0.0, epsilon=1.0, taps=taps)
        elif type == "Fading":
            channel1 = channels.channel_model_make(noise_voltage=noise_amplitude, frequency_offset=0.0, epsilon=1.0, taps=LTE_models.AWGN)
            channel2 = channels.fading_model_make(N=8, fDTs=0.0, LOS=True, K=3, seed=0)



        # add noise to ofdm signal
        add = blocks.add_cc_make()

        # demodulate noisy signal
        demod = dab.ofdm_demod_cc(dp)
        qpsk1 = dab_research.qpsk_demod_vcvb_make()
        qpsk2 = dab_research.qpsk_demod_vcvb_make()
        v2s_qpsk1 = blocks.vector_to_stream_make(gr.sizeof_char, 3072)
        v2s_qpsk2 = blocks.vector_to_stream_make(gr.sizeof_char, 3072)

        # data sinks
        pack1 = blocks.unpacked_to_packed_bb_make(1, gr.GR_MSB_FIRST)
        fic_sink = blocks.vector_sink_b_make()
        pack2 = blocks.unpacked_to_packed_bb_make(1, gr.GR_MSB_FIRST)
        msc_sink = blocks.vector_sink_b_make()
        null_sink = blocks.null_sink_make(gr.sizeof_gr_complex * 1536)

        head1 = blocks.head_make(gr.sizeof_char, 384*75*iterations*10)
        head2 = blocks.head_make(gr.sizeof_char, 3072*3*iterations)
        head3 = blocks.head_make(gr.sizeof_char, 3072*72*iterations)

        # connect everything
        self.connect(data_source, unpack_ref, ref_data_sink)
        #self.connect(data_source, s2v, mod, add, demod, qpsk1, v2s_qpsk1, head2, fic_sink)
        #self.connect(data_source, s2v, mod, channel, demod, qpsk1, v2s_qpsk1, head2, fic_sink)
        self.connect(data_source, s2v, mod, channel2, add, demod, qpsk1, v2s_qpsk1, head2, fic_sink)
        self.connect((demod, 1), qpsk2, v2s_qpsk2, head3, msc_sink)
        self.connect(noise_source, (add, 1))
        self.connect(trigsrc, (mod, 1))
        self.run()
        self.ref_data = ref_data_sink.data()
        self.ref = np.asarray(self.ref_data)
        self.ref = self.ref[0:iterations*3072*75]
        #print "ref bytes: " + str(self.ref)
        self.fic_data = fic_sink.data()
        self.fic = np.asarray(self.fic_data)
        #print "FIC bits: " + str(self.fic)
        self.msc_data = msc_sink.data()
        self.msc = np.asarray(self.msc_data)
        #print "MSC bits: " + str(self.msc)
        self.result = np.zeros(iterations*3072*75)
        for i in range(0, iterations):
            self.result[i*3072*75:i*3072*75+3072*3] = self.fic[i*3072*3 : 3072*3*i + 3072*3]
            self.result[i*3072*75 + 3*3072 : i*3072*75 + 75*3072] = self.msc[i * 3072 * 72: 3072 * 72 * (i + 1)]
        #print "output: " + str(self.result)
        self.error_rate = 1.0 - np.sum(self.result == self.ref)/(iterations*3072*75.0)
        print "SNR " + str(SNR) + ", BER = " + str(self.error_rate)

def calc_BER(noise_range, taps, type):
    BER = np.zeros(len(noise_range))
    for i, SNR in enumerate(noise_range):
        flowgraph = loopback(SNR, taps, type)
        BER[i] = flowgraph.error_rate
    print "BER = " + str(BER)
    return BER

# CONFIG #############################################################################################################
iterations = 30 #number of transmission frames
# SNR vector
SNR_range = np.arange(4.0, 10.0, 2.0)
# simulation types
types = {"AWGN", "Fading"}
######################################################################################################################

print "simulating AWGN model"
BER_AWGN = calc_BER(noise_range=SNR_range, taps=LTE_models.AWGN, type="Fading")
plt.semilogy(SNR_range, BER_AWGN, 'r')
np.savetxt("results/BER_AWGN.dat", np.c_[SNR_range, BER_AWGN], delimiter=' ')

# print "simulating LTE EPA model"
# BER_EPA = calc_BER(noise_range=SNR_range, taps=LTE_models.EPA_samp, type="Fading")
# plt.semilogy(SNR_range, BER_EPA, 'b')
# np.savetxt("results/BER_AWGN_LTE_EPA.dat", np.c_[SNR_range, BER_EPA], delimiter=' ')
#
# print "simulating LTE EVA model"
# BER_EVA = calc_BER(noise_range=SNR_range, taps=LTE_models.EVA_samp, type="Fading")
# plt.semilogy(SNR_range, BER_EVA, 'g')
# np.savetxt("results/BER_AWGN_LTE_EVA.dat", np.c_[SNR_range, BER_EVA], delimiter=' ')
#
# print "simulating LTE ETU model"
# BER_ETU = calc_BER(noise_range=SNR_range, taps=LTE_models.ETU_samp, type="Fading")
# plt.semilogy(SNR_range, BER_ETU, 'm')
# np.savetxt("results/BER_AWGN_LTE_ETU.dat", np.c_[SNR_range, BER_ETU], delimiter=' ')

plt.show()