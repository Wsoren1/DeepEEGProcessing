import sys


def write_to_file(source, target_dir, desired_samples):
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
        print(sample)
        samples += [sample]

    for sample_number in range(desired_samples):
        with open(target_dir + '\\' + str(sample_number), 'w') as f:
            for row in samples[sample_number]:
                f.writelines(row)


if __name__ == '__main__':
    source_file = sys.argv[1]
    target_dir = sys.argv[2]
    n_samples = int(sys.argv[3])

    write_to_file(source_file, target_dir, n_samples)
