
import os
import re


def load_file_as_values(file_name):
    file_to_load = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'samples',
                                file_name + '.txt')
    if os.path.exists(file_to_load):
        with open(file_to_load, 'rt') as f:
            content = f.read()
        return re.sub('(\||-)', '', content).replace('\n', ' ').replace('  ', ' ').split(' ')
    else:
        raise Exception("The file '{}' does not exist in 'samples' directory, please check your folder".
                        format(file_name))
