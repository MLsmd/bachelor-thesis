#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Nov  3 22:17:33 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import audio
from gnuradio import blocks
from gnuradio import channels
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import dab
import sip
import sys


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.sro_std = sro_std = 0
        self.sro_max = sro_max = 0
        self.samp_rate = samp_rate = 2048000
        self.doppler = doppler = 0.0
        self.cfo_std = cfo_std = 0
        self.cfo_max = cfo_max = 0
        self.SNR = SNR = 60

        ##################################################
        # Blocks
        ##################################################
        self._sro_std_range = Range(0, 100000, 1, 0, 200)
        self._sro_std_win = RangeWidget(self._sro_std_range, self.set_sro_std, "sro_std", "counter_slider", float)
        self.top_layout.addWidget(self._sro_std_win)
        self._sro_max_range = Range(0, 10000, 1, 0, 200)
        self._sro_max_win = RangeWidget(self._sro_max_range, self.set_sro_max, "sro_max", "counter_slider", float)
        self.top_layout.addWidget(self._sro_max_win)
        self._doppler_range = Range(0, 20.0, 1.0, 0.0, 200)
        self._doppler_win = RangeWidget(self._doppler_range, self.set_doppler, "doppler", "counter_slider", float)
        self.top_layout.addWidget(self._doppler_win)
        self._cfo_std_range = Range(0, 1000, 1, 0, 200)
        self._cfo_std_win = RangeWidget(self._cfo_std_range, self.set_cfo_std, "cfo_std", "counter_slider", float)
        self.top_layout.addWidget(self._cfo_std_win)
        self._cfo_max_range = Range(0, 10000, 1, 0, 200)
        self._cfo_max_win = RangeWidget(self._cfo_max_range, self.set_cfo_max, "cfo_max", "counter_slider", float)
        self.top_layout.addWidget(self._cfo_max_win)
        self._SNR_range = Range(0, 100, 1, 60, 200)
        self._SNR_win = RangeWidget(self._SNR_range, self.set_SNR, "SNR", "counter_slider", float)
        self.top_layout.addWidget(self._SNR_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_const_sink_x_1 = qtgui.const_sink_c(
        	1024, #size
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_1.set_update_time(0.10)
        self.qtgui_const_sink_x_1.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_1.enable_autoscale(False)
        self.qtgui_const_sink_x_1.enable_grid(False)
        
        if not True:
          self.qtgui_const_sink_x_1.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_1_win = sip.wrapinstance(self.qtgui_const_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_1_win)
        self.dab_ofdm_demod_cc_0 = dab.ofdm_demod_cc(
                  dab.parameters.dab_parameters(
                    mode=1,
                    sample_rate=samp_rate,
                    verbose=False
                  )
                )
          
        self.dab_fic_decode_vc_0 = dab.fic_decode_vc(dab.parameters.dab_parameters(mode=1, sample_rate=samp_rate, verbose=False))
        self.dab_dabplus_audio_decoder_ff_0 = dab.dabplus_audio_decoder_ff(dab.parameters.dab_parameters(mode=1, sample_rate=samp_rate, verbose=False), 112, 0, 84, 2, True)
        self.channels_dynamic_channel_model_0 = channels.dynamic_channel_model( samp_rate, sro_std, sro_max, cfo_std, cfo_max, 8, doppler, True, 4.0, ([0, 60, 160]), ([1.0, 0.5, 0.5]), 1, 10**((-34.4220877-SNR)/20.0), 0 )
        self.blocks_vector_to_stream_0_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1536)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1536)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1536)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, "/home/luca/bachelor-thesis/python/data/pure_dab.dat", True)
        self.audio_sink_0 = audio.sink(32000, "", True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.channels_dynamic_channel_model_0, 0))    
        self.connect((self.blocks_vector_to_stream_0, 0), (self.qtgui_const_sink_x_1, 0))    
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_null_sink_1, 0))    
        self.connect((self.blocks_vector_to_stream_0_1, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.channels_dynamic_channel_model_0, 0), (self.dab_ofdm_demod_cc_0, 0))    
        self.connect((self.dab_dabplus_audio_decoder_ff_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.dab_dabplus_audio_decoder_ff_0, 1), (self.audio_sink_0, 1))    
        self.connect((self.dab_ofdm_demod_cc_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.dab_ofdm_demod_cc_0, 1), (self.blocks_vector_to_stream_0_0, 0))    
        self.connect((self.dab_ofdm_demod_cc_0, 0), (self.blocks_vector_to_stream_0_1, 0))    
        self.connect((self.dab_ofdm_demod_cc_0, 1), (self.dab_dabplus_audio_decoder_ff_0, 0))    
        self.connect((self.dab_ofdm_demod_cc_0, 0), (self.dab_fic_decode_vc_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_sro_std(self):
        return self.sro_std

    def set_sro_std(self, sro_std):
        self.sro_std = sro_std
        self.channels_dynamic_channel_model_0.set_sro_dev_std(self.sro_std)

    def get_sro_max(self):
        return self.sro_max

    def set_sro_max(self, sro_max):
        self.sro_max = sro_max
        self.channels_dynamic_channel_model_0.set_sro_dev_max(self.sro_max)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.channels_dynamic_channel_model_0.set_samp_rate(self.samp_rate)

    def get_doppler(self):
        return self.doppler

    def set_doppler(self, doppler):
        self.doppler = doppler
        self.channels_dynamic_channel_model_0.set_doppler_freq(self.doppler)

    def get_cfo_std(self):
        return self.cfo_std

    def set_cfo_std(self, cfo_std):
        self.cfo_std = cfo_std
        self.channels_dynamic_channel_model_0.set_cfo_dev_std(self.cfo_std)

    def get_cfo_max(self):
        return self.cfo_max

    def set_cfo_max(self, cfo_max):
        self.cfo_max = cfo_max
        self.channels_dynamic_channel_model_0.set_cfo_dev_max(self.cfo_max)

    def get_SNR(self):
        return self.SNR

    def set_SNR(self, SNR):
        self.SNR = SNR
        self.channels_dynamic_channel_model_0.set_noise_amp(10**((-34.4220877-self.SNR)/20.0))


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
