#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sudoku_funcs import *

DEBUG = False


def num_cell_constraints(i, j):
    """
    1 value allowed for cells in the body, 0 values allowed for "holes" 
    """
    mid = [9, 10, 11]
    inset = []
    inset += [0, 1, 2, 3, 4, 5]   # top / left
    inset += [15, 16, 17, 18, 19, 20]  # bottom / right
    return 1 - (i in inset and j in mid) - (i in mid and j in inset)


def add_clues(model, flags, fname):
    with open(fname, 'r') as f:
        for i, line in enumerate(f):
            for j, cell in enumerate(line):
                try:
                    v = int(cell)
                    model += flags[i][j][v] == 1, f'Cell_{i:02d}_{j:02d}_{v}'
                except ValueError:
                    pass


def print_solution(flags, n_cols_rows, values, count):
    print('')
    print(f'Solution: #{count}')
    print('')

    # Create a solution
    for i in range(n_cols_rows):
        sol = ''
        for j in range(n_cols_rows):
            val = " "
            for v in values:
                if value(flags[i][j][v]) == 1:
                    val = str(v)
                    break
            sol += " {0}".format(val)
        print(sol)


def solve_sudoku(fname, n_cols_rows, values):

    # Prepare the model and  the flags
    model, flags = init_model(f'Sudoku {fname} Model', n_cols_rows, values, num_cell_constraints)

    # Set Column, Row, and Square constraints
    for v in values:

        # Set constraints in upper and lower blocks
        for a in range(n_cols_rows):
            mk_column_constraint(model, flags, v, 0, a)
            mk_row_constraint(model, flags, v, a, 0)

        # Set 3x3 square constraints
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                mk_square_constraint(model, flags, v, i, j)

    # Add the clues
    add_clues(model, flags, fname)

    # Debugging: Write the lp problem model
    if DEBUG:
        model.writeLP(f'{fname}.lp')

    # Find all solutions
    count = 0
    while True:
        model.solve()

        # Exit when no more 'optimal' solutions are available
        if model.status != 1:
            break

        count += 1

        # Print the solution
        print_solution(flags, n_cols_rows, values, count)

        # Add a new constraint to forbid finding this solution again
        model += lpSum([flags[i][j][v] for i in range(n_cols_rows) for j in range(n_cols_rows)
                       for v in values if value(flags[i][j][v]) == 1]) <= 80

    print(f'\n{count} solution(s) found.')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        this = os.path.basename(sys.argv[0])
        print(f'Usage: ./{this} filename.sudoku')
        quit()

    ncr = 9
    vals = list(range(1, 10))
    solve_sudoku(sys.argv[1], ncr, vals)
