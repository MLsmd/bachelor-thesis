#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Wed Oct 11 20:28:48 2017
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
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import dab
import dab_research
import sip
import sys
import time


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
        self.samp_rate = samp_rate = 2048000
        self.gain_slider = gain_slider = 50

        ##################################################
        # Blocks
        ##################################################
        self._gain_slider_range = Range(0, 100, 1, 50, 200)
        self._gain_slider_win = RangeWidget(self._gain_slider_range, self.set_gain_slider, "gain", "counter_slider", float)
        self.top_layout.addWidget(self._gain_slider_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_clock_rate(samp_rate*20, uhd.ALL_MBOARDS)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(208064000, 0)
        self.uhd_usrp_source_0.set_gain(gain_slider, 0)
        self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
        	2552*4, #size
        	samp_rate, #samp_rate
        	"", #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(0, 1.2)
        
        self.qtgui_time_sink_x_1.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0.003, 1, "Start of Frame")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_1.disable_legend()
        
        labels = ["Power", "Correlation", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 3, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [0.2, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win, 0,0,1,2)
        self.qtgui_const_sink_x_3_0_0_0 = qtgui.const_sink_c(
        	1024, #size
        	"after time and fine and coarse freq sync", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_3_0_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_3_0_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_3_0_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_3_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_3_0_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_3_0_0_0.enable_grid(False)
        
        if not True:
          self.qtgui_const_sink_x_3_0_0_0.disable_legend()
        
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
                self.qtgui_const_sink_x_3_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_3_0_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_3_0_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_3_0_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_3_0_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_3_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_3_0_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_3_0_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_3_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_3_0_0_0_win, 1,0,1,1)
        self.qtgui_const_sink_x_3_0_0 = qtgui.const_sink_c(
        	1024, #size
        	"IQ data", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_3_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_3_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_3_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_3_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_3_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_3_0_0.enable_grid(False)
        
        if not True:
          self.qtgui_const_sink_x_3_0_0.disable_legend()
        
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
                self.qtgui_const_sink_x_3_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_3_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_3_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_3_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_3_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_3_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_3_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_3_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_3_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_3_0_0_win, 0,2,1,1)
        self.qtgui_const_sink_x_3_0 = qtgui.const_sink_c(
        	1024, #size
        	"extracted channel", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_3_0.set_update_time(0.10)
        self.qtgui_const_sink_x_3_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_3_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_3_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_3_0.enable_autoscale(False)
        self.qtgui_const_sink_x_3_0.enable_grid(False)
        
        if not True:
          self.qtgui_const_sink_x_3_0.disable_legend()
        
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
                self.qtgui_const_sink_x_3_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_3_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_3_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_3_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_3_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_3_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_3_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_3_0_win = sip.wrapinstance(self.qtgui_const_sink_x_3_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_3_0_win, 1,2,1,1)
        self.qtgui_const_sink_x_3 = qtgui.const_sink_c(
        	1024, #size
        	"after diff phasor", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_3.set_update_time(0.10)
        self.qtgui_const_sink_x_3.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_3.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_3.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_3.enable_autoscale(False)
        self.qtgui_const_sink_x_3.enable_grid(False)
        
        if not True:
          self.qtgui_const_sink_x_3.disable_legend()
        
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
                self.qtgui_const_sink_x_3.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_3.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_3.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_3.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_3.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_3.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_3.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_3_win = sip.wrapinstance(self.qtgui_const_sink_x_3.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_3_win, 1,1,1,1)
        self.fft_vxx_0 = fft.fft_vcc(2048, True, ([]), True, 1)
        self.dab_research_delayed_correlation_cc_0 = dab_research.delayed_correlation_cc()
        self.dab_ofdm_synchronization_cvf_0 = dab.ofdm_synchronization_cvf(2048, 504, 2048, 76)
        self.dab_ofdm_coarse_frequency_correction_vcvc_0 = dab.ofdm_coarse_frequency_correction_vcvc(2048, 1536, 504)
        self.dab_diff_phasor_vcc_0_0 = dab.diff_phasor_vcc(1536)
        self.dab_demux_cc_0 = dab.demux_cc(1536, 3, 72, 0)
        self.blocks_vector_to_stream_0_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1536)
        self.blocks_vector_to_stream_0_0_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1536)
        self.blocks_vector_to_stream_0_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1536)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1536)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 2048)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((500, ))
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_time_sink_x_1, 1))    
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_1, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.blocks_vector_to_stream_0_0_0, 0), (self.qtgui_const_sink_x_3_0_0_0, 0))    
        self.connect((self.blocks_vector_to_stream_0_0_0_0, 0), (self.qtgui_const_sink_x_3, 0))    
        self.connect((self.blocks_vector_to_stream_0_1, 0), (self.qtgui_const_sink_x_3_0, 0))    
        self.connect((self.dab_demux_cc_0, 0), (self.blocks_vector_to_stream_0_0, 0))    
        self.connect((self.dab_demux_cc_0, 1), (self.blocks_vector_to_stream_0_1, 0))    
        self.connect((self.dab_diff_phasor_vcc_0_0, 0), (self.blocks_vector_to_stream_0_0_0_0, 0))    
        self.connect((self.dab_diff_phasor_vcc_0_0, 0), (self.dab_demux_cc_0, 0))    
        self.connect((self.dab_ofdm_coarse_frequency_correction_vcvc_0, 0), (self.blocks_vector_to_stream_0_0_0, 0))    
        self.connect((self.dab_ofdm_coarse_frequency_correction_vcvc_0, 0), (self.dab_diff_phasor_vcc_0_0, 0))    
        self.connect((self.dab_ofdm_synchronization_cvf_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.dab_research_delayed_correlation_cc_0, 0), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.dab_ofdm_coarse_frequency_correction_vcvc_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.dab_ofdm_synchronization_cvf_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.dab_research_delayed_correlation_cc_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_const_sink_x_3_0_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_gain_slider(self):
        return self.gain_slider

    def set_gain_slider(self, gain_slider):
        self.gain_slider = gain_slider
        self.uhd_usrp_source_0.set_gain(self.gain_slider, 0)
        	


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
