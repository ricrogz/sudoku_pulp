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


def add_clues(model, flags, clues):
    for i, line in enumerate(clues):
        for j, cell in enumerate(line):
            if cell in ('.', ' '):
                continue
            v = int(cell)
            model += flags[i][j][v] == 1, f'Cell_{i:02d}_{j:02d}_{v}'


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


def solve_samurai(clues, n_cols_rows, values):

    # Prepare the model and  the flags
    model, flags = init_model(f'Samurai Model', n_cols_rows, values, num_cell_constraints)

    # Set Column, Row, and Square constraints
    for v in values:

        # Set constraints in upper and lower blocks
        for a in [0, 12]:
            for b in [0, 12]:
                for c in range(b, b + 9):
                    mk_column_constraint(model, flags, v, a, c)
                    mk_row_constraint(model, flags, v, c, a)

        # Set row constraints for central block:
        for a in range(6, 6 + 9):
            mk_column_constraint(model, flags, v, 6, a)
            mk_row_constraint(model, flags, v, a, 6)

        # Set 3x3 square constraints
        for i in range(0, 21, 3):
            for j in range(0, 21, 3):
                if (i in [0, 3, 15, 18] and j == 9) or (i == 9 and j in [0, 3, 15, 18]):
                    continue
                mk_square_constraint(model, flags, v, i, j)

    # Add the clues
    add_clues(model, flags, clues)

    # Debugging: Write the lp problem model
    if DEBUG:
        model.writeLP(f'Samurai_Model.lp')

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
                       for v in values if value(flags[i][j][v]) == 1]) <= 368

    print(f'\n{count} solution(s) found.')


if __name__ == '__main__':
    ncr = 21
    vals = list(range(1, 10))

    # Get clues
    if len(sys.argv) < 2:
        clue_lines = read_input(ncr)
    else:
        clue_lines = read_file(sys.argv[1], ncr)

    solve_samurai(clue_lines, ncr, vals)
