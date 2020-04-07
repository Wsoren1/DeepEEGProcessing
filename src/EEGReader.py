import numpy as np
import csv


class EEGReader:
    def __init__(self, fname):
        with open(fname, 'r') as f:
            reader = csv.reader(f)
            channels = []
            for row in reader:
                channels += [row[1:9]]

        with open(fname, 'r') as f:
            sample_line = None
            for i, line in enumerate(f):
                if i == 2:
                    sample_line = line
                elif i > 6:
                    break

        channels = np.array(channels[6:])  # Remove headlines
        channels = channels.astype(np.float)

        self.board_sample_rate = int(float(sample_line.split(' ')[3]))
        self.channels = channels