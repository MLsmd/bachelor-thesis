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
    def __init__(self, power, SNR, doppler):
        gr.top_block.__init__(self)
        dp = dab.parameters.dab_parameters(mode=1, sample_rate=2048000, verbose=False)

        data_source = blocks.file_source_make(gr.sizeof_gr_complex, "data/gen_iq_A1_A3.dat", False)
        noise_amplitude = 10 ** ((power - SNR) / 20.0)
        noise_source = analog.noise_source_c_make(analog.GR_GAUSSIAN, noise_amplitude)
        add = blocks.add_cc_make()
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

        demod = dab.ofdm_demod_cc(dp)
        fic_decode = dab_research.fic_decode_vc(dp)
        fic_sink = dab_research.measure_fib_error_rate_make()
        msc_null = blocks.null_sink_make(gr.sizeof_gr_complex*1536)
        head_syms = blocks.head_make(gr.sizeof_gr_complex * 1536, iterations/4+reserve/4)
        head_iterations = blocks.head_make(gr.sizeof_char, iterations)
        sink = blocks.vector_sink_b_make()

        self.connect(data_source, add, demod, head_syms, fic_decode, fic_sink, head_iterations, sink)
        self.connect((demod, 1), msc_null)
        #self.connect(head_iq, delay2, channel2, (add, 1))
        #self.connect(head_iq, delay3, channel3, (add, 2))
        self.connect(noise_source, (add, 1))
        self.run()
        result = np.array(sink.data())
        successes = np.count_nonzero(result)
        if len(result) != iterations:
            self.fail_rate = -1
            print "ERROR, result is shorter than input vector (" + str(len(result)) + ")"
        else:
            self.fail_rate = 1 - float(successes) / iterations
            print "PER = " + str(self.fail_rate) + " SNR = " + str(SNR) + ", doppler = " + str(doppler)


# measure power of iq_data
iq_gen = np.fromfile('data/gen_iq_A1_A3.dat', dtype=np.complex64, count=10000000)
power = 10 * np.log10(np.mean(np.square(np.absolute(iq_gen))))
print "power = " + str(power)

# calculate FIC error rate
def calc_PER(noise_range, doppler):
    BER = np.zeros(len(noise_range))
    for i, SNR in enumerate(noise_range):
        flowgraph = loopback(power, SNR, doppler)
        BER[i] = flowgraph.fail_rate
    print "total results: BER = " + str(BER) + " for Doppler = " + str(doppler) + " +++++++++++++++++++++++"
    return BER


# settings ##########################
iterations = 10000
reserve = 100
noise_range = np.arange(0.0, 1.0, 1.0)
#doppler_range = np.arange(5.0, 200.0, 180.0)
doppler_range = np.array([5.5])
#####################################
plot = plt.figure()

for doppler in doppler_range:
    BER_array = calc_PER(noise_range, doppler)
    plt.semilogy(noise_range, BER_array)
    np.savetxt("results/AWGN/171108_AWGN_PER_FIC.dat", np.c_[noise_range, BER_array], delimiter=' ')
    print "final result for doppler = " + str(doppler) + ": " + str(BER_array)

plt.show()
