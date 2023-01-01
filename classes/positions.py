
from random import shuffle


def retrieve_row_id_from_position_and_size(position, size):
    return position // size


def retrieve_column_id_from_position_and_size(position, size):
    return position % size


def retrieve_grid_id_from_row_and_col(row_id, col_id, grid_size):
    return int(col_id // grid_size + ((row_id // grid_size) * grid_size))


def retrieve_range_rows_from_grid_id(grid_id, grid_size):
    start = int(grid_id / grid_size) * grid_size
    return range(start, start + grid_size)


def retrieve_range_columns_from_grid_id(grid_id, grid_size):
    start = int(grid_id % grid_size) * grid_size
    return range(start, start + grid_size)


def retrieve_row_id_from_grid_id_and_position(grid_id, grid_position, grid_size):
    row_in_grid = retrieve_row_id_from_position_and_size(grid_position, grid_size)
    delta_row = grid_size * (retrieve_row_id_from_position_and_size(grid_id, grid_size))
    return delta_row + row_in_grid


def retrieve_column_id_from_grid_id_and_position(grid_id, grid_position, grid_size):
    col_in_grid = retrieve_column_id_from_position_and_size(grid_position, grid_size)
    delta_col = grid_size * (retrieve_column_id_from_position_and_size(grid_id, grid_size))
    return delta_col + col_in_grid


def fill_with_some_valid_values(array_to_fill, length):
    # Get fixed values
    fixed_values = [value for value in array_to_fill if value > 0]
    # Get fixed values and their index
    fixed_index_values = [(pos, value) for pos, value in enumerate(array_to_fill) if value > 0]
    # Determine what are the available values based on fixed values
    available_values = [x for x in range(1, length + 1) if x not in fixed_values]
    shuffle(available_values)
    # Add fixed values in the shuffled array
    for index, val in fixed_index_values:
        available_values.insert(index, val)
    return available_values
