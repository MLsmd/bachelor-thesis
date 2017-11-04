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
    def __init__(self, SNR, type, doppler, seed):
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

        channel = channels.dynamic_channel_model_make(samp_rate=2048000,
                                                      sro_std_dev=0.0,
                                                      sro_max_dev=0.0,
                                                      cfo_std_dev=0.0,
                                                      cfo_max_dev=0.0,
                                                      N=8,
                                                      doppler_freq=doppler,
                                                      LOS_model=False,
                                                      K=4.0,
                                                      delays=[0.0],
                                                      mags=[1.0],
                                                      ntaps_mpath=1,
                                                      noise_amp=noise_amplitude,
                                                      noise_seed=seed
                                                      )
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

        head1 = blocks.head_make(gr.sizeof_char, 384*75*iterations*2)
        head2 = blocks.head_make(gr.sizeof_char, 3072*3*iterations)
        head3 = blocks.head_make(gr.sizeof_char, 3072*72*iterations)

        # connect everything
        if type == "Dynamic":
            self.connect(data_source, s2v, mod, channel, demod, qpsk1, v2s_qpsk1, head2, fic_sink)
        if type == "AWGN":
            self.connect(data_source, s2v, mod, add, demod, qpsk1, v2s_qpsk1, head2, fic_sink)
            self.connect(noise_source, (add, 1))
        self.connect(data_source, unpack_ref, ref_data_sink)
        #self.connect(data_source, s2v, mod, add, demod, qpsk1, v2s_qpsk1, head2, fic_sink)
        #self.connect(data_source, s2v, mod, channel, demod, qpsk1, v2s_qpsk1, head2, fic_sink)
        self.connect((demod, 1), qpsk2, v2s_qpsk2, head3, msc_sink)

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

def calc_BER(noise_range, type, doppler, seed):
    BER = np.zeros(len(noise_range))
    for i, SNR in enumerate(noise_range):
        flowgraph = loopback(SNR, type, doppler, seed)
        BER[i] = flowgraph.error_rate
    print "BER = " + str(BER)
    return BER


# CONFIG #############################################################################################################
iterations = 100 #number of transmission frames
# SNR vector
SNR_range = np.arange(10.0, 40.0, 4.0)
# doppler vector
freq_range = np.arange(0.0, 50.0, 5.0)
# simulation types
types = {"AWGN", "Fading"}
######################################################################################################################
print "simulating dynamic fading model, no doppler"
BER_AWGN = calc_BER(noise_range=SNR_range, type="Dynamic", doppler=0.0, seed=0)
plt.semilogy(SNR_range, BER_AWGN, 'b')
#np.savetxt("results/BER_Dynamic_Fading.dat", np.c_[SNR_range, BER_AWGN], delimiter=' ')

print "simulating dynamic fading model, no doppler"
BER_AWGN = calc_BER(noise_range=SNR_range, type="Dynamic", doppler=0.0, seed=1)
plt.semilogy(SNR_range, BER_AWGN, 'b')
#np.savetxt("results/BER_Dynamic_Fading.dat", np.c_[SNR_range, BER_AWGN], delimiter=' ')

print "simulating dynamic fading model, no doppler"
BER_AWGN = calc_BER(noise_range=SNR_range, type="Dynamic", doppler=0.0, seed=1)
plt.semilogy(SNR_range, BER_AWGN, 'b')
#np.savetxt("results/BER_Dynamic_Fading.dat", np.c_[SNR_range, BER_AWGN], delimiter=' ')
plt.show()
print "simulating dynamic fading model, doppler = 10"
BER_AWGN = calc_BER(noise_range=SNR_range, type="Dynamic", doppler=10.0, seed=0)
plt.semilogy(SNR_range, BER_AWGN, 'r')
#np.savetxt("results/BER_Dynamic_Fading.dat", np.c_[SNR_range, BER_AWGN], delimiter=' ')

print "simulating dynamic fading model, doppler = 102"
BER_AWGN = calc_BER(noise_range=SNR_range, type="Dynamic", doppler=10.0, seed=0)
plt.semilogy(SNR_range, BER_AWGN, 'r')
#np.savetxt("results/BER_Dynamic_Fading.dat", np.c_[SNR_range, BER_AWGN], delimiter=' ')

print "simulating dynamic fading model, doppler = 102"
BER_AWGN = calc_BER(noise_range=SNR_range, type="Dynamic", doppler=10.0, seed=1)
plt.semilogy(SNR_range, BER_AWGN, 'r')
#np.savetxt("results/BER_Dynamic_Fading.dat", np.c_[SNR_range, BER_AWGN], delimiter=' ')
plt.show()
print "simulating dynamic fading model"
BER_AWGN = calc_BER(noise_range=SNR_range, type="Dynamic", doppler=20.0,seed=0)
plt.semilogy(SNR_range, BER_AWGN, 'g')
#np.savetxt("results/BER_Dynamic_Fading.dat", np.c_[SNR_range, BER_AWGN], delimiter=' ')

print "simulating dynamic fading model"
BER_AWGN = calc_BER(noise_range=SNR_range, type="Dynamic", doppler=20.0,seed=1)
plt.semilogy(SNR_range, BER_AWGN, 'g')
#np.savetxt("results/BER_Dynamic_Fading.dat", np.c_[SNR_range, BER_AWGN], delimiter=' ')

print "simulating dynamic fading model"
BER_AWGN = calc_BER(noise_range=SNR_range, type="Dynamic", doppler=20.0, seed=1)
plt.semilogy(SNR_range, BER_AWGN, 'g')
#np.savetxt("results/BER_Dynamic_Fading.dat", np.c_[SNR_range, BER_AWGN], delimiter=' ')
plt.show()
print "simulating dynamic fading model"
BER_AWGN = calc_BER(noise_range=SNR_range, type="Dynamic", doppler=30.0,seed=0)
plt.semilogy(SNR_range, BER_AWGN, 'y')
#np.savetxt("results/BER_Dynamic_Fading.dat", np.c_[SNR_range, BER_AWGN], delimiter=' ')

print "simulating dynamic fading model"
BER_AWGN = calc_BER(noise_range=SNR_range, type="Dynamic", doppler=30.0,seed=1)
plt.semilogy(SNR_range, BER_AWGN, 'y')
#np.savetxt("results/BER_Dynamic_Fading.dat", np.c_[SNR_range, BER_AWGN], delimiter=' ')

print "simulating dynamic fading model"
BER_AWGN = calc_BER(noise_range=SNR_range, type="Dynamic", doppler=30.0, seed=1)
plt.semilogy(SNR_range, BER_AWGN, 'y')
#np.savetxt("results/BER_Dynamic_Fading.dat", np.c_[SNR_range, BER_AWGN], delimiter=' ')
plt.show()