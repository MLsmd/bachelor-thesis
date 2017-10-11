#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Delayed Correlation
# Generated: Wed Oct 11 19:33:06 2017
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
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import sys
import time


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
        self.mult_const = mult_const = 50
        self.gain_slider = gain_slider = 50

        ##################################################
        # Blocks
        ##################################################
        self._gain_slider_range = Range(0, 100, 1, 50, 200)
        self._gain_slider_win = RangeWidget(self._gain_slider_range, self.set_gain_slider, "gain_slider", "counter_slider", float)
        self.top_layout.addWidget(self._gain_slider_win)
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0_0.set_clock_rate(20*samp_rate, uhd.ALL_MBOARDS)
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_0.set_center_freq(208064000, 0)
        self.uhd_usrp_source_0_0.set_gain(gain_slider, 0)
        self.uhd_usrp_source_0_0.set_antenna("TX/RX", 0)
        self._mult_const_range = Range(0, 1000, 10, 50, 200)
        self._mult_const_win = RangeWidget(self._mult_const_range, self.set_mult_const, "energy_normalization", "counter_slider", float)
        self.top_layout.addWidget(self._mult_const_win)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "/home/luca/Desktop/iq_dab/171011.dat", False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0_0, 0), (self.blocks_file_sink_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "delayed_correlation")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)

    def get_mult_const(self):
        return self.mult_const

    def set_mult_const(self, mult_const):
        self.mult_const = mult_const

    def get_gain_slider(self):
        return self.gain_slider

    def set_gain_slider(self, gain_slider):
        self.gain_slider = gain_slider
        self.uhd_usrp_source_0_0.set_gain(self.gain_slider, 0)
        	


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
