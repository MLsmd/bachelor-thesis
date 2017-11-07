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

iterations = 10000

'''
measure the rate of passed and failed FICs (validated over CRC check)
'''

class loopback(gr.top_block):
    def __init__(self, power, SNR, doppler):
        gr.top_block.__init__(self)
        dp = dab.parameters.dab_parameters(mode=1, sample_rate=2048000, verbose=False)

        data_source = blocks.file_source_make(gr.sizeof_gr_complex, "data/pure_dab_long.dat", True)
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
        head_iq = blocks.head_make(gr.sizeof_gr_complex, iterations * 16384)
        ok_sink = blocks.vector_sink_b_make()
        fail_sink = blocks.vector_sink_b_make()
        self.connect(data_source, head_iq, channel1, add, demod, fic_decode, fic_sink, ok_sink)
        self.connect((demod, 1), msc_null)
        self.connect((fic_sink, 1), fail_sink)
        self.connect(head_iq, delay2, channel2, (add, 1))
        self.connect(head_iq, delay3, channel3, (add, 2))
        self.connect(noise_source, (add, 3))
        self.run()
        self.ok_data = np.asarray(ok_sink.data())
        self.fail_data = np.asarray(fail_sink.data())
        print "simulating SNR = " + str(SNR) + "###Doppler = " + str(doppler) + "#############"
        print "passed: " + str(np.count_nonzero(self.ok_data)) + "von" + str(len(self.ok_data))
        print "failed: " + str(np.count_nonzero(self.fail_data)) + "von" + str(len(self.fail_data))


# measure power of iq_data
iq_gen = np.fromfile('data/pure_dab_long.dat', dtype=np.complex64, count=10000000)
power = 10 * np.log10(np.mean(np.square(np.absolute(iq_gen))))
print "power = " + str(power)

# calculate FIC error rate
def calc_FIC_errors(noise_range, doppler):

    successes = np.zeros(len(noise_range))
    fails = np.zeros(len(noise_range))
    for i, SNR in enumerate(noise_range):
        flowgraph = loopback(power, SNR, doppler)
        # calculate variance and std
        successes[i] = np.count_nonzero(flowgraph.ok_data)
        fails[i] = np.count_nonzero(flowgraph.fail_data)
        i += 1

    print "############################################################################ RESULTS"
    print "ok: " + str(successes)
    print "fails: " + str(fails)
    # num_fibs because every frame passes sync at 60 dB
    print ""
    print "absolute fails:  " + str(fails)
    print "absolute suc:    " + str(successes)
    print "fail rate:       " + str(np.divide(fails,fails+successes))
    return np.divide(fails, fails+successes)

# SNR vector
SNR_range = np.arange(3.0, 40.0, 4.0)
# doppler vector
doppler_range = np.arange(5.0, 6.0, 20.0)

results = np.zeros((len(doppler_range), len(SNR_range)))

for x, doppler in enumerate(doppler_range):
    results[x] = calc_FIC_errors(SNR_range, doppler)
    np.savetxt("results/multipath/171107_fic_error_rate_doppler" + str(doppler) + ".dat", np.c_[SNR_range, results[x]], delimiter=' ')

luca = plt.figure()

# print data
for x, doppler in enumerate(doppler_range):
    plt.plot(SNR_range, results[x])

plt.show()
print "final results"
print results

#np.savetxt("results/fic_successes.dat", np.c_[noise_range, successes], delimiter=' ')
#np.savetxt("results/fic_fails.dat", np.c_[noise_range, fails], delimiter=' ')
