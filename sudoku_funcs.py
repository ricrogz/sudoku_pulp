#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pulp import *


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
