from data_pre_processing.src.pre_processing import write_to_file
import os

# def write_to_file(source, target_dir, desired_samples, percent_val)

source_dirs = []
class_names = []
target_dir = input('target_dir : ')

while True:
    source_dirs += [input('source_dir : ')]
    class_names += [input('class_name : ')]

    if input("[y/n] Add_another_class? : ").lower() == 'n':
        break

n_samples = float(input('sample_len  : '))
percent_val = int(input('percent_val: ')) / 100

for i in range(len(source_dirs)):
    for file in os.listdir(source_dirs[i]):
        write_to_file(source_dirs[i] + "/" + file, target_dir, n_samples, percent_val, class_names[i])
