# Author: Walker Sorensen
import sys
import os
import shutil
from random import randrange
from datetime import datetime


def write_to_file(source, target_dir, desired_sample_length, percent_val, class_name):
    with open(source, 'r') as f:
        rows = [line for line in f]
    size = len(rows) - 6
    headers = rows[:6]
    total_seconds = (datetime.strptime(rows[-2].split(',')[12], " %H:%M:%S.%f") -
                     datetime.strptime(rows[7].split(',')[12], " %H:%M:%S.%f")).total_seconds()

    if sample_length > total_seconds:
        raise Exception("sample_length larger than length of file: " + source)

    desired_samples = int(total_seconds / desired_sample_length)
    step = size / desired_samples

    samples = []
    for i in range(desired_samples):
        sample = []
        sample += [row for row in headers]
        sample += [rows[int(i * step + 6):int(step + i * step)]]
        samples += [sample]

    if not os.path.exists(target_dir + "\\validation"):
        os.makedirs(target_dir + "\\validation\\")
        os.makedirs(target_dir + "\\train\\")

    if not os.path.exists(target_dir + "\\validation\\" + class_name):
        os.makedirs(target_dir + "\\validation\\" + class_name)
        os.makedirs(target_dir + "\\train\\" + class_name)

    for sample_number in range(desired_samples):
        with open(target_dir + '\\' + str(sample_number), 'w') as f:
            for row in samples[sample_number]:
                f.writelines(row)

    val_last_num = len(os.listdir(target_dir + "\\validation\\" + class_name))
    train_last_num = len(os.listdir(target_dir + "\\train\\" + class_name))

    i = 0
    dirs = os.listdir(target_dir)[:-2]
    while len(dirs) > 0:
        file = dirs[randrange(0, len(dirs))]

        if i < desired_samples * percent_val:
            shutil.move(target_dir + '\\' + file,
                        target_dir + "\\validation\\" + class_name + "\\" + str(i + val_last_num))
        else:
            shutil.move(target_dir + '\\' + file,
                        target_dir + "\\train\\" + class_name + "\\" +
                        str(int(i - desired_samples * percent_val + train_last_num)))

        i += 1
        dirs = os.listdir(target_dir)[:-2]


if __name__ == '__main__':
    source_file = sys.argv[1]
    target_dir = sys.argv[2]
    class_name = sys.argv[3]
    sample_length = float(sys.argv[4])
    percent_val = float(sys.argv[5])

    write_to_file(source_file, target_dir, sample_length, percent_val, class_name)
