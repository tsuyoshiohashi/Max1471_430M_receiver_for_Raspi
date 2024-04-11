#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: 432M_Tx_afsk
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import sip



class Pluto_432M_tx_afsk(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "432M_Tx_afsk", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("432M_Tx_afsk")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "Pluto_432M_tx_afsk")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.sel_sig = sel_sig = 4
        self.samp_rate = samp_rate = 96000
        self.rf_freq = rf_freq = 433890000
        self.rf_att = rf_att = 50
        self.freq_cutoff = freq_cutoff = 7500
        self.fdev = fdev = 3500
        self.f_amp = f_amp = 0.5

        ##################################################
        # Blocks
        ##################################################

        # Create the options list
        self._sel_sig_options = [0, 1, 2, 3, 4]
        # Create the labels list
        self._sel_sig_labels = ['CW(continious wave)', 'data_0(2200Hz)', 'data_1(1200Hz)', 'data_1010', 'Char_A']
        # Create the combo box
        self._sel_sig_tool_bar = Qt.QToolBar(self)
        self._sel_sig_tool_bar.addWidget(Qt.QLabel("Sel_Sig" + ": "))
        self._sel_sig_combo_box = Qt.QComboBox()
        self._sel_sig_tool_bar.addWidget(self._sel_sig_combo_box)
        for _label in self._sel_sig_labels: self._sel_sig_combo_box.addItem(_label)
        self._sel_sig_callback = lambda i: Qt.QMetaObject.invokeMethod(self._sel_sig_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._sel_sig_options.index(i)))
        self._sel_sig_callback(self.sel_sig)
        self._sel_sig_combo_box.currentIndexChanged.connect(
            lambda i: self.set_sel_sig(self._sel_sig_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._sel_sig_tool_bar)
        self._rf_freq_range = Range(433750000, 433960000, 5000, 433890000, 200)
        self._rf_freq_win = RangeWidget(self._rf_freq_range, self.set_rf_freq, "RF_FREQ", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rf_freq_win)
        self._rf_att_range = Range(40, 60, 1, 50, 200)
        self._rf_att_win = RangeWidget(self._rf_att_range, self.set_rf_att, "RF_ATT", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rf_att_win)
        self._freq_cutoff_range = Range(5000, 10000, 500, 7500, 200)
        self._freq_cutoff_win = RangeWidget(self._freq_cutoff_range, self.set_freq_cutoff, "freq_cutoff", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_cutoff_win)
        self._fdev_range = Range(2000, 6000, 500, 3500, 200)
        self._fdev_win = RangeWidget(self._fdev_range, self.set_fdev, "freq_deviation", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._fdev_win)
        self._f_amp_range = Range(0, 1, 0.1, 0.5, 200)
        self._f_amp_win = RangeWidget(self._f_amp_range, self.set_f_amp, "FAMP", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._f_amp_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                freq_cutoff,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.iio_pluto_sink_0 = iio.fmcomms2_sink_fc32('192.168.2.1' if '192.168.2.1' else iio.get_pluto_uri(), [True, True], 1024, False)
        self.iio_pluto_sink_0.set_len_tag_key('')
        self.iio_pluto_sink_0.set_bandwidth(20000000)
        self.iio_pluto_sink_0.set_frequency(rf_freq)
        self.iio_pluto_sink_0.set_samplerate(samp_rate)
        self.iio_pluto_sink_0.set_attenuation(0, rf_att)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', 0, 0)
        self.blocks_vector_source_x_0 = blocks.vector_source_f((1,1,1,1,1,0,1,0,0,0,0,0,1,0), True, 1, [])
        self.blocks_vco_f_0 = blocks.vco_f(samp_rate, 15708, f_amp)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,sel_sig,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, 80)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((-0.4))
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(0.88)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_SQR_WAVE, 600, 0.4, 0.48, 0)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=samp_rate,
        	quad_rate=samp_rate,
        	tau=(75e-6),
        	max_dev=fdev,
        	fh=(-1.0),
                )
        self.analog_const_source_x_1 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0.48)
        self.analog_const_source_x_0_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0.88)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.analog_const_source_x_1, 0), (self.blocks_selector_0, 2))
        self.connect((self.analog_nbfm_tx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_selector_0, 3))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_selector_0, 4))
        self.connect((self.blocks_selector_0, 0), (self.blocks_vco_f_0, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.analog_nbfm_tx_0, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Pluto_432M_tx_afsk")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sel_sig(self):
        return self.sel_sig

    def set_sel_sig(self, sel_sig):
        self.sel_sig = sel_sig
        self._sel_sig_callback(self.sel_sig)
        self.blocks_selector_0.set_input_index(self.sel_sig)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.iio_pluto_sink_0.set_samplerate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.freq_cutoff, 1000, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_rf_freq(self):
        return self.rf_freq

    def set_rf_freq(self, rf_freq):
        self.rf_freq = rf_freq
        self.iio_pluto_sink_0.set_frequency(self.rf_freq)

    def get_rf_att(self):
        return self.rf_att

    def set_rf_att(self, rf_att):
        self.rf_att = rf_att
        self.iio_pluto_sink_0.set_attenuation(0,self.rf_att)

    def get_freq_cutoff(self):
        return self.freq_cutoff

    def set_freq_cutoff(self, freq_cutoff):
        self.freq_cutoff = freq_cutoff
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.freq_cutoff, 1000, window.WIN_HAMMING, 6.76))

    def get_fdev(self):
        return self.fdev

    def set_fdev(self, fdev):
        self.fdev = fdev
        self.analog_nbfm_tx_0.set_max_deviation(self.fdev)

    def get_f_amp(self):
        return self.f_amp

    def set_f_amp(self, f_amp):
        self.f_amp = f_amp




def main(top_block_cls=Pluto_432M_tx_afsk, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
