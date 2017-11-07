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
class measure_power(gr.top_block):
    def __init__(self, mean_iterations):
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
        add = blocks.add_cc_make()

        # channel model
        channel1 = channels.dynamic_channel_model_make(samp_rate=2048000,
                                                       sro_std_dev=0.0,
                                                       sro_max_dev=0.0,
                                                       cfo_std_dev=0.0,
                                                       cfo_max_dev=0.0,
                                                       N=8,
                                                       doppler_freq=5.0,
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
                                                       doppler_freq=5.0,
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
                                                       doppler_freq=5.0,
                                                       LOS_model=False,
                                                       K=4.0,
                                                       delays=[0],
                                                       mags=[0.4],
                                                       ntaps_mpath=1,
                                                       noise_amp=0.0,
                                                       noise_seed=0
                                                       )



        # data sink
        sink = blocks.vector_sink_c_make()
        head = blocks.head_make(gr.sizeof_gr_complex, mean_iterations)

        # connect everything
        self.connect(data_source, pack, s2v, mod, channel1, add)
        self.connect(trigsrc, (mod, 1))
        self.connect(mod, delay2, channel2, (add, 1))
        self.connect(mod, delay3, channel3, (add, 2))
        self.connect(add, head, sink)
        self.run()
        data = sink.data()
        self.power = 10 * np.log10(np.mean(np.square(np.absolute(data))))

    def get_power(self):
        print "power = " + str(self.power)
        return self.power