#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pulp import *


CLUE_CHARS = re.compile(r'[^ .\d]')


def init_model(name, n_cols_rows, values, n_constraints_func):
    # Create the model
    model = LpProblem(name, LpMinimize)
    model += 0, "Empty Objective Function"

    # Build a 3D array value x rows x cols
    n_rows_cols = list(range(n_cols_rows))
    flags = LpVariable.dicts("Flags", (n_rows_cols, n_rows_cols, values), 0, 1, LpInteger)

    # Allow only 1 value per cell and 0 in empty spaces
    for i in range(n_cols_rows):
        for j in range(n_cols_rows):
            model += lpSum([flags[i][j][v] for v in values]) == n_constraints_func(i, j), f'Cell_{i:02d}_{j:02d}_v'

    return model, flags


def mk_column_constraint(model, flags, v, i, j):
    model += lpSum([flags[ii][j][v] for ii in range(i, i + 9)]) == 1, f'9Col_{i:02d}_{j:02d}_{v}'


def mk_row_constraint(model, flags, v, i, j):
    model += lpSum([flags[i][jj][v] for jj in range(j, j + 9)]) == 1, f'9Row_{i:02d}_{j:02d}_{v}'


def mk_square_constraint(model, flags, v, i, j):
    model += lpSum([flags[ii][jj][v] for ii in range(i, i + 3) for jj in range(j, j + 3)]) == 1,\
             f'9Sq_{i:02d}_{j:02d}_{v}'


def validate_clue_line(txt):
    """ Validate clue line agains allowed characters. Exit if not valid chars found. """
    if CLUE_CHARS.search(txt):
        print('ERROR: unexpected characters in clue line "{txt}".')
        quit()


def read_file(fname, ncr):
    """ Read the clues from a file """
    print(f'Reading clues from {fname}...')
    clues = []
    with open(fname, 'r') as f:
        for line in f:
            clue = line.rstrip()
            validate_clue_line(clue)
            clues.append(clue)

    if len(clues) < ncr:
        print(f'Input error: insufficient lines in input.\nPlease provide {ncr} lines of data.')
        quit()
    return clues


def read_input(ncr):
    """ Get clues from stdin. An appropriate number of lines must be provided """
    print('No input file specified; entering interactive mode.')
    print('Please paste sudoku below.')
    clues = []
    try:
        for _ in range(ncr):
            clue = input().rstrip()
            validate_clue_line(clue)
            clues.append(clue)
    except IndexError:
        print(f'Input error: insufficient lines in input.\nPlease provide {ncr} lines of data.')
        quit()
    return clues
