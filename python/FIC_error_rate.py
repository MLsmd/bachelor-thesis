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
from gnuradio import channels
import matplotlib.pyplot as plt
import dab
import dab_research
import DAB_channels



'''
measure the rate of passed and failed FICs (validated over CRC check)
'''

class loopback(gr.top_block):
    def __init__(self, SNR, doppler):
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
        fic_decode = dab_research.fic_decode_vc(dp)
        fic_sink = dab_research.measure_fib_error_rate_make()
        msc_null = blocks.null_sink_make(gr.sizeof_gr_complex*1536)
        head_syms = blocks.head_make(gr.sizeof_gr_complex * 1536, iterations/4+reserve/4)
        head_iterations = blocks.head_make(gr.sizeof_char, iterations)
        sink = blocks.vector_sink_b_make()

        self.connect(data_source, channel1, add, demod, head_syms, fic_decode, fic_sink, head_iterations, sink)
        self.connect((demod, 1), msc_null)
        self.connect(data_source, delay2, channel2, (add, 1))
        self.connect(data_source, delay3, channel3, (add, 2))
        self.connect(noise_source, (add, 3))
        self.run()
        result = np.array(sink.data())
        successes = np.count_nonzero(result)
        if len(result) != iterations:
            self.fail_rate = -1
            print "ERROR, result is shorter than input vector (" + str(len(result)) + ")"
        else:
            self.fail_rate = 1 - float(successes) / iterations
            print "PER = " + str(self.fail_rate) + " SNR = " + str(SNR) + ", doppler = " + str(doppler)

# calculate FIC error rate
def calc_PER(noise_range, doppler):
    PER_multi = np.zeros((repetitions, len(noise_range)))
    PER = np.zeros(len(noise_range))
    for j in range(0, repetitions, 1):
        for i, SNR in enumerate(noise_range):
            flowgraph = loopback(SNR, doppler)
            PER[i] = flowgraph.fail_rate
        PER_multi[j] = PER
        print "finished repetition " + str(j)
    print "multi PER = " + str(PER_multi)
    PER = np.mean(PER_multi, axis=0)
    print "total results: PER = " + str(PER) + " for Doppler = " + str(doppler) + " +++++++++++++++++++++++"
    return PER


# settings ##########################
iterations = 1000
reserve = 100
repetitions = 100
noise_range = np.arange(5.0, 41.0, 5.0)
#doppler_range = np.arange(5.0, 200.0, 180.0)
doppler_range = np.array([5.0])
#####################################
plot = plt.figure()

for doppler in doppler_range:
    PER_array = calc_PER(noise_range, doppler)
    plt.semilogy(noise_range, PER_array)
    np.savetxt("results/171115_dynamic_doppler_" + str(doppler) + "_FIC.dat", np.c_[noise_range, PER_array], delimiter=' ')
    print "final result for doppler = " + str(doppler) + ": " + str(PER_array)

plt.show()
