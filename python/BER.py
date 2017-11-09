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
import measure_Power
'''
Messung der BER des physical channels
'''
class loopback(gr.top_block):
    def __init__(self, power, SNR, doppler):
        gr.top_block.__init__(self)
        dp = dab.parameters.dab_parameters(mode=1, sample_rate=2048000, verbose=False)

        # random but known bit data as source
        random_bit_vector = np.random.randint(low=0, high=2, size=3072)
        data_source = blocks.vector_source_b_make(random_bit_vector, True)
        pack = blocks.unpacked_to_packed_bb_make(1, gr.GR_MSB_FIRST)
        s2v = blocks.stream_to_vector_make(gr.sizeof_char, 384)
        trigsrc = blocks.vector_source_b([1] + [0] * (dp.symbols_per_frame - 2), True)

        # ofdm mod
        mod = dab.ofdm_mod(dp)

        # noise source
        noise_amplitude = 10**((power-SNR)/20.0)
        noise_source = analog.noise_source_c_make(analog.GR_GAUSSIAN, noise_amplitude)
        add = blocks.add_cc_make()

        # channel model
        channel1 = channels.dynamic_channel_model_make(samp_rate=2048000,
                                                       sro_std_dev=0.0,
                                                       sro_max_dev=0.0,
                                                       cfo_std_dev=0.0,
                                                       cfo_max_dev=0.0,
                                                       N=8,
                                                       doppler_freq=doppler,
                                                       LOS_model=False,
                                                       K=4.0,
                                                       delays=[0],
                                                       mags=[1.0],
                                                       ntaps_mpath=1,
                                                       noise_amp=0.0,
                                                       noise_seed=0
                                                       )
        delay2 = blocks.delay_make(gr.sizeof_gr_complex, 60)
        channel2 = channels.dynamic_channel_model_make(samp_rate=2048000,
                                                       sro_std_dev=0.0,
                                                       sro_max_dev=0.0,
                                                       cfo_std_dev=0.0,
                                                       cfo_max_dev=0.0,
                                                       N=8,
                                                       doppler_freq=doppler,
                                                       LOS_model=False,
                                                       K=4.0,
                                                       delays=[0],
                                                       mags=[0.5],
                                                       ntaps_mpath=1,
                                                       noise_amp=0.0,
                                                       noise_seed=0
                                                       )
        delay3 = blocks.delay_make(gr.sizeof_gr_complex, 160)
        channel3 = channels.dynamic_channel_model_make(samp_rate=2048000,
                                                       sro_std_dev=0.0,
                                                       sro_max_dev=0.0,
                                                       cfo_std_dev=0.0,
                                                       cfo_max_dev=0.0,
                                                       N=8,
                                                       doppler_freq=doppler,
                                                       LOS_model=False,
                                                       K=4.0,
                                                       delays=[0],
                                                       mags=[0.4],
                                                       ntaps_mpath=1,
                                                       noise_amp=0.0,
                                                       noise_seed=0
                                                       )


        # demodulate noisy signal
        demod = dab.ofdm_demod_cc(dp)
        qpsk = dab_research.qpsk_demod_vcvb_make()
        v2s_qpsk = blocks.vector_to_stream_make(gr.sizeof_char, 3072)

        # data sinks
        fic_null_sink = blocks.null_sink_make(gr.sizeof_gr_complex * 1536)
        head = blocks.head_make(gr.sizeof_char, iterations)
        msc_sink = blocks.vector_sink_b_make()

        # connect everything
        self.connect(data_source, pack, s2v, mod, channel1, add)
        self.connect(trigsrc, (mod, 1))
        self.connect(mod, delay2, channel2, (add, 1))
        self.connect(mod, delay3, channel3, (add, 2))
        self.connect(noise_source, (add, 3))
        self.connect(add, demod, fic_null_sink)
        self.connect((demod, 1), qpsk, v2s_qpsk, head, msc_sink)
        self.run()
        # results
        result = np.array(msc_sink.data())
        successes = np.sum(result == np.tile(random_bit_vector, symbols))
        if len(result) != iterations:
            self.fail_rate = -1
            print "ERROR, result is shorter than input vector"
        else:
            self.fail_rate = 1 - float(successes) / iterations
            print "BER = " + str(self.fail_rate) + " SNR = " + str(SNR) + ", doppler = " + str(doppler)

def calc_BER(Power, noise_range, doppler):
    BER_multi = np.zeros((repetitions, len(noise_range)))
    BER = np.zeros(len(noise_range))
    for j in range(0, repetitions, 1):
        for i, SNR in enumerate(noise_range):
            flowgraph = loopback(Power, SNR, doppler)
            BER[i] = flowgraph.fail_rate
        BER_multi[j] = BER
        print "finished repetition " + str(j)
    print "multi BER = " + str(BER_multi)
    BER = np.mean(BER_multi, axis=0)
    print "total results: BER = " + str(BER) + " for Doppler = " + str(doppler) + " +++++++++++++++++++++++"
    return BER

# settings ##########################
symbols = 10000
iterations = symbols * 3072
repetitions = 50
noise_range = np.arange(33.0, 34.0, 4.0)
#doppler_range = np.arange(5.0, 200.0, 180.0)
doppler_range = np.array([5.0])
power_meter = measure_Power.measure_power(1000000)
power = power_meter.get_power()
#####################################
plot = plt.figure()

for doppler in doppler_range:
    BER_array = calc_BER(power, noise_range, doppler)
    plt.semilogy(noise_range, BER_array)
    np.savetxt("results/multipath/BER/171109_BER_dynamic_doppler_" + str(doppler) + ".dat", np.c_[noise_range, BER_array], delimiter=' ')
    print "final result for doppler = " + str(doppler) + ": " + str(BER_array)

plt.show()
