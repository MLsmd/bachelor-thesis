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
from gnuradio import channels
import matplotlib.pyplot as plt


'''
measure the rate of passed and failed firecodes
'''

class loopback(gr.top_block):
    def __init__(self, SNR, doppler, protection, address, size):
        gr.top_block.__init__(self)
        dp = dab.parameters.dab_parameters(mode=1, sample_rate=2048000, verbose=False)

        data_source = blocks.file_source_make(gr.sizeof_gr_complex, "data/pure_dab_norm.dat", False)
        noise_amplitude = 10 ** ((-SNR) / 20.0)
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
                                                       mags=[0.686],
                                                       ntaps_mpath=1,
                                                       noise_amp=0.0,
                                                       noise_seed=np.random.random_sample() * (-10 ** (5))
                                                       )
        delay2 = blocks.delay_make(gr.sizeof_gr_complex, 40)
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
                                                       mags=[0.514],
                                                       ntaps_mpath=1,
                                                       noise_amp=0.0,
                                                       noise_seed=np.random.random_sample() * (-10 ** (5))
                                                       )
        delay3 = blocks.delay_make(gr.sizeof_gr_complex, 80)
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
                                                       mags=[0.514],
                                                       ntaps_mpath=1,
                                                       noise_amp=0.0,
                                                       noise_seed=np.random.random_sample() * (-10 ** (5))
                                                       )

        demod = dab.ofdm_demod_cc(dp)
        msc_decode = dab.msc_decode(dp, address, size, protection)
        fic_null = blocks.null_sink_make(gr.sizeof_gr_complex*1536)
        firecode = dab_research.firecode_check_bb_make(14)
        head_syms = blocks.head_make(gr.sizeof_gr_complex * 1536, iterations * 72/4 + reserve * 72/4)
        head_iterations = blocks.head_make(gr.sizeof_char, iterations+15) # the first 15 firecodes fail because of time_interleaver
        ok_sink = blocks.vector_sink_b_make()

        self.connect(data_source, channel1, add, demod, fic_null)
        self.connect((demod, 1), head_syms, msc_decode, firecode, head_iterations, ok_sink)
        self.connect(data_source, delay2, channel2, (add, 1))
        self.connect(data_source, delay3, channel3, (add, 2))
        self.connect(noise_source, (add, 3))
        self.run()
        result = np.asarray(ok_sink.data())
        if len(result) != iterations+15:
            self.fail_rate = -1
            print "ERROR, result is shorter than input vector (" + str(len(result)) + ")"
        else:
            successes = np.count_nonzero(result[15:])
            self.fail_rate = 1 - float(successes) / iterations
            print "PER = " + str(self.fail_rate) + " SNR = " + str(SNR) + ", doppler = " + str(doppler)

# calculate MSC Firecode error rate
def calc_PER(noise_range, doppler, protection, address, size):
    PER_multi = np.zeros((repetitions, len(noise_range)))
    PER = np.zeros(len(noise_range))
    for j in range(0, repetitions, 1):
        for i, SNR in enumerate(noise_range):
            flowgraph = loopback(SNR, doppler, protection, address, size)
            PER[i] = flowgraph.fail_rate
        PER_multi[j] = PER
        print "finished repetition " + str(j)
    print "multi PER = " + str(PER_multi)
    PER = np.mean(PER_multi, axis=0)
    print "total results: PER = " + str(PER) + " for Doppler = " + str(doppler) + " +++++++++++++++++++++++"
    return PER


# settings ##########################
iterations = 4000
reserve = 50
repetitions = 2
noise_range = np.arange(40.0, 41.0, 20.0)
#doppler_range = np.arange(5.0, 200.0, 180.0)
doppler_range = np.array([5.0, 10.0, 20.0, 50.0])
#####################################
plot = plt.figure()

for doppler in doppler_range:
    PER_array = calc_PER(noise_range, doppler, 2, 0, 84)
    np.savetxt("results/171115_dynamic_doppler_" + str(doppler) + "_MSC_A3.dat", np.c_[noise_range, PER_array], delimiter=' ')
    plt.semilogy(noise_range, PER_array)
    print "final result for doppler = " + str(doppler) + ": " + str(PER_array)

plt.show()

