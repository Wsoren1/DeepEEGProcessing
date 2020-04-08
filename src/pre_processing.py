import sys
import os
import shutil
from random import randrange


def write_to_file(source, target_dir, desired_samples, percent_val):
    with open(source, 'r') as f:
        rows = [line for line in f]
    size = len(rows) - 6
    step = size/desired_samples
    headers = rows[:6]

    samples = []
    for i in range(desired_samples):
        sample = []
        sample += [row for row in headers]
        sample += [rows[int(i*step+6):int(step+i*step)]]
        samples += [sample]

    for sample_number in range(desired_samples):
        with open(target_dir + '\\' + str(sample_number), 'w') as f:
            for row in samples[sample_number]:
                f.writelines(row)

    os.makedirs(target_dir + "\\validation")
    os.makedirs(target_dir + "\\train")

    i = 0
    dirs = os.listdir(target_dir)[:-2]
    while len(dirs) > 0:
        file = dirs[randrange(0, len(dirs))]

        if i < desired_samples * percent_val:
            shutil.move(target_dir + '\\' + file,
                        target_dir + "\\validation\\" + str(i))
        else:
            shutil.move(target_dir + '\\' + file,
                        target_dir + "\\train\\" + str(int(i - desired_samples * percent_val)))

        i += 1
        dirs = os.listdir(target_dir)[:-2]


if __name__ == '__main__':
    source_file = sys.argv[1]
    target_dir = sys.argv[2]
    n_samples = int(sys.argv[3])
    percent_val = float(sys.argv[4])

    if n_samples * percent_val - int(n_samples * percent_val) != 0:
        raise Exception("n_samples * percent_val != int()")
    if os.listdir(target_dir) != []:
        raise Exception("Target directory not empty")

    write_to_file(source_file, target_dir, n_samples, percent_val)
