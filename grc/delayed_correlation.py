#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Delayed Correlation
# Generated: Tue Nov 14 18:08:01 2017
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
from gnuradio import analog
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


class delayed_correlation(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Delayed Correlation")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Delayed Correlation")
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

        self.settings = Qt.QSettings("GNU Radio", "delayed_correlation")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2048000
        self.doppler = doppler = 0
        self.SNR = SNR = 50

        ##################################################
        # Blocks
        ##################################################
        self._doppler_range = Range(0, 100, 1, 0, 200)
        self._doppler_win = RangeWidget(self._doppler_range, self.set_doppler, "doppler", "counter_slider", float)
        self.top_layout.addWidget(self._doppler_win)
        self._SNR_range = Range(-20, 100, 1, 50, 200)
        self._SNR_win = RangeWidget(self._SNR_range, self.set_SNR, "SNR", "counter_slider", float)
        self.top_layout.addWidget(self._SNR_win)
        self.qtgui_time_sink_x_1_0 = qtgui.time_sink_f(
        	1024*10, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_1_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_1_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_1_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_0_win)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
        	1024, #size
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(False)
        
        if not True:
          self.qtgui_const_sink_x_0_0.disable_legend()
        
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
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_0_win)
        self.dab_ofdm_demod_cc_0 = dab.ofdm_demod_cc(
                  dab.parameters.dab_parameters(
                    mode=1,
                    sample_rate=samp_rate,
                    verbose=False
                  )
                )
          
        self.channels_dynamic_channel_model_0_0_0 = channels.dynamic_channel_model( samp_rate, 0.0, 0.0, 0.0, 0.0, 8, doppler, True, 4.0, ([0]), ([0.514]), 1, 0.0, -657 )
        self.channels_dynamic_channel_model_0_0 = channels.dynamic_channel_model( samp_rate, 0.0, 0.0, 0.0, 0.0, 8, doppler, True, 4.0, ([0]), ([0.514]), 1, 0.0, -657 )
        self.channels_dynamic_channel_model_0 = channels.dynamic_channel_model( samp_rate, 0.0, 0.0, 0.0, 0.0, 8, doppler, False, 4.0, ([0]), ([0.686]), 1, 0.0, -65432 )
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1536)
        self.blocks_rms_xx_0_0 = blocks.rms_cf(1e-6)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1536)
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, "/home/luca/bachelor-thesis/python/data/pure_dab_norm.dat", True)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 2)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_fastnoise_source_x_0 = analog.fastnoise_source_c(analog.GR_GAUSSIAN, 10**((-SNR)/20.0), 0, 8192)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fastnoise_source_x_0, 0), (self.blocks_add_xx_0, 3))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_rms_xx_0_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.dab_ofdm_demod_cc_0, 0))    
        self.connect((self.blocks_delay_0, 0), (self.channels_dynamic_channel_model_0_0, 0))    
        self.connect((self.blocks_delay_0_0, 0), (self.channels_dynamic_channel_model_0_0_0, 0))    
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_delay_0, 0))    
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_delay_0_0, 0))    
        self.connect((self.blocks_file_source_0_0, 0), (self.channels_dynamic_channel_model_0, 0))    
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_nlog10_ff_0_0, 0))    
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.qtgui_time_sink_x_1_0, 0))    
        self.connect((self.blocks_rms_xx_0_0, 0), (self.blocks_multiply_xx_0_0, 0))    
        self.connect((self.blocks_rms_xx_0_0, 0), (self.blocks_multiply_xx_0_0, 1))    
        self.connect((self.blocks_vector_to_stream_1, 0), (self.qtgui_const_sink_x_0_0, 0))    
        self.connect((self.channels_dynamic_channel_model_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.channels_dynamic_channel_model_0_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.channels_dynamic_channel_model_0_0_0, 0), (self.blocks_add_xx_0, 2))    
        self.connect((self.dab_ofdm_demod_cc_0, 1), (self.blocks_null_sink_0, 0))    
        self.connect((self.dab_ofdm_demod_cc_0, 0), (self.blocks_vector_to_stream_1, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "delayed_correlation")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_1_0.set_samp_rate(self.samp_rate)
        self.channels_dynamic_channel_model_0.set_samp_rate(self.samp_rate)
        self.channels_dynamic_channel_model_0_0.set_samp_rate(self.samp_rate)
        self.channels_dynamic_channel_model_0_0_0.set_samp_rate(self.samp_rate)

    def get_doppler(self):
        return self.doppler

    def set_doppler(self, doppler):
        self.doppler = doppler
        self.channels_dynamic_channel_model_0.set_doppler_freq(self.doppler)
        self.channels_dynamic_channel_model_0_0.set_doppler_freq(self.doppler)
        self.channels_dynamic_channel_model_0_0_0.set_doppler_freq(self.doppler)

    def get_SNR(self):
        return self.SNR

    def set_SNR(self, SNR):
        self.SNR = SNR
        self.analog_fastnoise_source_x_0.set_amplitude(10**((-self.SNR)/20.0))


def main(top_block_cls=delayed_correlation, options=None):

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
