
from random import randint

from math import sqrt
import numpy as np

from classes import positions, s_utils, tools
inner = []

class Sudoku(object):


    _grid_size = 0
    _size = 0
    _fixed_values = None
    _rows = None
    _columns = None
    _grids = None
    _fitness_score = None

    def __init__(self, values):



        nb_rows = int(sqrt(len(values)))
        self._size = nb_rows
        self._grid_size = int(sqrt(nb_rows))
        self._rows = {}
        self._columns = {}
        self._grids = {}
        self._fixed_values = {}

        if nb_rows/self._grid_size != self._grid_size:
            raise Exception("You must provide a power number value")

        self._init_values = []
        self.set_initial_values(values)

    def set_initial_values(self, values):

        self._init_values = values
        expected_len = pow(self._size, 2)
        if len(values) != expected_len:
            raise Exception("You must provide a number of values matching the size of the objects. Got {} whereas {} "
                            "was expected".format(len(values), expected_len))

        # Init the dicts
        for i in range(self._size):
            self._rows[i] = []
            self._columns[i] = []
            self._grids[i] = []

        # In the above section we determine, according to the position in the given values, in which
        # column, row and grid the value belongs to
        position = 0
        for character in values:
            val = int(character)
            row_id = positions.retrieve_row_id_from_position_and_size(position, self._size)
            col_id = positions.retrieve_column_id_from_position_and_size(position, self._size)
            grid_id = positions.retrieve_grid_id_from_row_and_col(row_id, col_id, self._grid_size)

            position += 1

            # Add this value to all dicts we maintain
            self._rows[row_id].append(val)
            self._columns[col_id].append(val)
            self._grids[grid_id].append(val)

            # Keep knowledge of fixed values where key is their position (key= row_id|col_id)
            if val != 0:
                self._fixed_values[s_utils.build_fixed_val_key(row_id, col_id)] = val
        return self

    def fill_random(self):

        # Ensure that at least grids are 'correct' so we fill each one with available values to avoid duplicates
        for grid_id, grid_values in self._grids.items():
            available_values = positions.fill_with_some_valid_values(grid_values, self._size)

            # Get row and col from grid_id and position in grid and substitute the value
            for position, new_value in enumerate(available_values):
                row_id = positions.retrieve_row_id_from_grid_id_and_position(grid_id, position, self._grid_size)
                col_id = positions.retrieve_column_id_from_grid_id_and_position(grid_id, position, self._grid_size)
                self._columns[col_id][row_id] = new_value
                self._rows[row_id][col_id] = new_value

            # Substitute value with new one in grids arrays
            self._grids[grid_id] = available_values
        return self

    def fill_with_grids(self, grids):

        for grid_id, grid_values in enumerate(grids):
            # Get row and col from grid_id and position in grid and substitute the value
            for position, value in enumerate(grid_values):
                row_id = positions.retrieve_row_id_from_grid_id_and_position(grid_id, position, self._grid_size)
                col_id = positions.retrieve_column_id_from_grid_id_and_position(grid_id, position, self._grid_size)
                self._columns[col_id][row_id] = value
                self._rows[row_id][col_id] = value

                self._grids[grid_id][position] = value
        return self

    def display(self):



        for i in range(self._size):
            if i > 1 and i % self._grid_size == 0:
                print(s_utils.build_separator_line(self._grid_size))
            temp=[]
            line = self._rows[i]
            for j in range(self._size):
                val = line[j]


                if self.size() > 9:
                    val = str(val).zfill(2)

                if j > 0 and j % self._grid_size == 0:
                    print(' | {}'.format(val), end='')
                    temp.append(val)
                elif j == (self._size - 1):
                    print(' {}'.format(val))
                    temp.append(val)
                else:
                    print(' {}'.format(val), end='')
                    temp.append(val)

            inner.append(temp)
        print("")

        #print(inner)

    def grids(self):

        return self._grids

    def rows(self):

        return self._rows

    def columns(self):

        return self._columns

    def size(self):

        return self._size

    def grid_size(self):

        return self._grid_size

    def get_initial_values(self):

        return self._init_values

    def fitness(self):

        # Evaluate once per individual
        if self._fitness_score is None:
            duplicates_counter = 0
            for i in range(self.size()):
                duplicates_counter += tools.count_duplicates(self._rows[i]) + tools.count_duplicates(self._columns[i])
            self._fitness_score = duplicates_counter
        return self._fitness_score

    def swap_2_values(self):

        # Pick a random grid
        grid_id = np.random.randint(0, self._size - 1)

        rand_pos_1, row_id_1, col_id_1 = self._get_random_not_fixed(grid_id, -1)
        rand_pos_2, row_id_2, col_id_2 = self._get_random_not_fixed(grid_id, rand_pos_1)

        grid_values = self._grids[grid_id]
        val_1 = grid_values[rand_pos_1]
        val_2 = grid_values[rand_pos_2]

        grid_values[rand_pos_1] = val_2
        grid_values[rand_pos_2] = val_1
        self._rows[row_id_1][col_id_1] = val_2
        self._rows[row_id_2][col_id_2] = val_1
        self._columns[col_id_1][row_id_1] = val_2
        self._columns[col_id_2][row_id_2] = val_1

        return self

    def _is_fixed(self, row_id, col_id):

        return s_utils.build_fixed_val_key(row_id, col_id) in self._fixed_values

    def _get_random_not_fixed(self, grid_id, forbidden_pos):

        rand_pos = -1
        row_id = -1
        col_id = -1
        is_fixed = True
        while is_fixed or rand_pos == forbidden_pos:
            rand_pos = randint(0, self._size - 1)
            # We need to find their position (row and column) in the whole table to check whether it is fixed or not
            row_id = positions.retrieve_row_id_from_grid_id_and_position(grid_id, rand_pos, self._grid_size)
            col_id = positions.retrieve_column_id_from_grid_id_and_position(grid_id, rand_pos, self._grid_size)
            is_fixed = self._is_fixed(row_id, col_id)
        return rand_pos, row_id, col_id
