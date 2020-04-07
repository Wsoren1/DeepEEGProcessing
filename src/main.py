# Author: Walker Sorensen
#
# Parts of bandpass and notch functions use code from:
# https://github.com/J77M/openbciGui_filter_test/blob/master/gui_saved_data_filter.ipynb
import sys
import matplotlib.pyplot as plt
import numpy as np
from EEGReader import EEGReader
from scipy import signal
import copy


def plot_data(channels):
    fig, axs = plt.subplots(len(channels[0]), sharex=True)
    fig.suptitle('EEG Plot: ' + sys.argv[1])
    i = 0
    for ax in axs:
        ax.plot(channels[:, i])
        ax.set_ylabel('C ' + str(i + 1))
        ax.set_yticks([])
        i += 1

    plt.show()


def bandpass(channels):
    with open('src/filter_settings', 'r') as f:
        f.readline()
        bp_range = f.readline()[:-1]

    bp_range = tuple(map(int, bp_range[7:].split(',')))

    filtered_channels = copy.copy(channels)

    fs = 200
    bp_Hz = np.array([bp_range[0], bp_range[1]])
    b, a = signal.butter(5, bp_Hz / (fs / 2.0), btype='bandpass')

    for i in range(len(filtered_channels[0])):
        filtered_channels[:, i] = signal.lfilter(b, a, filtered_channels[:, i], axis=0)

    return filtered_channels


def notch(channels):
    with open('src/filter_settings', 'r') as f:
        notch_freq = int(f.readline()[7:-1])

    filtered_channels = copy.copy(channels)

    fs = 200
    for i in range(len(filtered_channels[0])):
        for freq in np.nditer(notch_freq):
            bp_stop = freq + 3.0 * np.array([-1, 1])
            b, a = signal.butter(3, bp_stop / (fs / 2.0), 'bandstop')
            filtered_channels[:, i] = signal.lfilter(b, a, filtered_channels[:, i])

    return filtered_channels


if __name__ == '__main__':
    reader = EEGReader(sys.argv[1])
    data = reader.channels

    for flag in sys.argv[1:]:
        if flag == '-b':
            data = bandpass(data)
            continue
        if flag == '-n':
            data = notch(data)
            continue
        if flag == '-p':
            plot_data(data)

