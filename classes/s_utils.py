

def build_fixed_val_key(row_id, col_id):

    return "[{}|{}]".format(str(row_id), str(col_id))


def build_separator_line(grid_size):

    seps = '--' * grid_size
    if grid_size > 3:
        seps += '----'
    separator_line = '{}-|'.format(seps) * grid_size
    return separator_line[:len(separator_line) - 1]
