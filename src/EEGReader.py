import numpy as np
import csv
import datetime


class EEGReader:
    def __init__(self, fname):
        with open(fname, 'r') as f:
            reader = csv.reader(f)
            channels = []
            timestamps = []
            for i in range(6):  # skips headers
                next(reader)

            for row in reader:
                channels += [row[1:9]]
                timestamps += [row[12]]

        with open(fname, 'r') as f:
            sample_line = None
            for i, line in enumerate(f):
                if i == 2:
                    sample_line = line
                elif i > 6:
                    break

        channels = np.array(channels[:])
        channels = channels.astype(np.float)

        timestamps = list(map(lambda x: datetime.datetime.strptime(x, ' %H:%M:%S.%f'), timestamps))
        starttime = timestamps[0]
        timestamps = np.array([timestamp - starttime for timestamp in timestamps])
        timestamps = [timestamp.total_seconds() for timestamp in timestamps]
        self.board_sample_rate = int(float(sample_line.split(' ')[3]))
        self.channels = channels
        self.timestamps = timestamps
