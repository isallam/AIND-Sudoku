assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
# Element example:
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# This is the top most row.

col_units = [cross(rows, c) for c in cols]
# Element example:
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
# This is the left most column.

square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# Element example:
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
# This is the top left square.

unitlist = row_units + col_units + square_units;

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for box in values.keys():
        if len(values[box]) == 2:
            twin_value = values[box]
            # check box units for naked twins
            for unit in units[box]:
                # check the unit for a valid twin.
                twins = [s for s in unit if len(values[s]) == 2 and values[s] == twin_value]
                if len(twins) == 2:
                    # Eliminate the naked twins as possibilities for boxes of a unit
                    for peer in unit:
                        if len(values[peer]) > 1 and peer not in twins:
                            new_value = ''.join([c for c in values[peer] if c not in twin_value])
                            assign_value(values, peer, new_value)

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)*3])
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for box in values.keys():
        if len(values[box]) == 1:
            to_eliminate = values[box]
            # eliminate the value from all peers
            for peer in peers[box]:
                new_value = values[peer].replace(to_eliminate, '')
                assign_value(values, peer, new_value)

    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for key in unit:
            if len(values[key]) > 1:
                for digit in values[key]:
                    # get a list of boxes that have digits from our selected box
                    only_choice_list = [box for box in unit if digit in values[box]]
                    if len(only_choice_list) == 1:
                        assign_value(values, only_choice_list[0], digit)
                        break
    return values


def is_solved(values):
    """ Check to see if all boxes have one digit in them.

     This assume that by applying constrains to solve the puzzle we'll only
     need to check if 81 single digit exist in the grid.
     We probably need a better verification to ensure that the rules are enforced

    Input: Sudoku in dictionary form.
    Output: True if all boxes have only 1 value.
    """
    return len([box for box in values.keys() if len(values[box]) == 1]) == 81


def is_error(values):
    return type(values) is bool and values is False


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.

    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # check if puzzle is solved
        if is_solved(values): return values

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        if is_solved(values): return values

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values


def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku."

    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if is_error(values):
        return False # failed to do early reduction

    if is_solved(values):
        return values # we're done

    # Choose one of the unfilled squares with the fewest possibilities
    list_of_keys = []
    min_possibility = 2
    while list_of_keys == []:
        list_of_keys = [box for box in values.keys() if len(values[box]) == min_possibility]
        min_possibility +=1


    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!

    for key in list_of_keys:
        for digit in values[key]:
            # make a copy for search trials.
            possible_solution = {k:v for k, v in values.items()}
            assign_value(possible_solution, key, digit)
            # # check to see if we have solution
            possible_solution = search(possible_solution)
            if is_error(possible_solution):
                continue # try the next digit
            if is_solved(possible_solution):
                return possible_solution

    return values


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    result = search(grid_values(grid))
    return result

if __name__ == '__main__':
    # grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    # display(solve(grid2))
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
