# Author: Walker Sorensen
import numpy as np
import csv
# import datetime
from scipy import signal
import copy
import sys
import matplotlib.pyplot as plt
import numpy as np


class EEGReader:
    def __init__(self, fname, filtered=False):
        with open(fname, 'r') as f:
            reader = csv.reader(f)
            channels = []
            # timestamps = []
            for i in range(6):  # skips headers
                next(reader)

            for row in reader:
                channels += [row[1:9]]
                # timestamps += [row[12]]

        with open(fname, 'r') as f:
            sample_line = None
            for i, line in enumerate(f):
                if i == 2:
                    sample_line = line
                elif i > 6:
                    break

        channels = np.array(channels[:])
        channels = channels.astype(np.float)

        # timestamps = list(map(lambda x: datetime.datetime.strptime(x, ' %H:%M:%S.%f'), timestamps))
        # starttime = timestamps[0]
        # timestamps = np.array([timestamp - starttime for timestamp in timestamps])
        # timestamps = [timestamp.total_seconds() for timestamp in timestamps]
        self.board_sample_rate = int(float(sample_line.split(' ')[3]))
        self.channels = channels
        # self.timestamps = timestamps

        if filtered:
            self.bandpass_self()
            self.notch_self()

    def bandpass_self(self):
        self.channels = self.bandpass(self.channels)
        return self.channels

    def notch_self(self):
        self.channels = self.notch(self.channels)

    def plot_self(self):
        self.plot_data(self.channels)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

