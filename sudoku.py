# -*- coding: utf-8 -*-

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
v =    '4.....8.5.3..........7......2.....6.....8.4...4..1.......6.3.7.5.32.1...1.4......'
def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(rows, cols)
    return dict((box,'123456789') if value == '.'  
                else (box,value)for (box,value) in zip(boxes, grid))


values_g = grid_values(grid)
values = grid_values(v)
def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for k,v in values.items():
        if len(v) == 1:
            for p in peers[k]:
                values[p] = values[p].replace(v,'')
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # TODO: Implement only choice strategy here
    
    for box, box_unit_lists in units.items():
        s = '123456789'
        if len(values[box])!=1:
            boxes = sum(box_unit_lists, [])
            for b in boxes:
                value = values[b]
                if len(value) == 1:
                    s = s.replace(value,'')
            if len(s) ==1:
                values[box] = s
                
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if not values:return False
        
    # Choose one of the unfilled squares with the fewest possibilities

    sorted_keys = [k for k in sorted(values, key=lambda k: len(values[k])) if len(values[k]) !=1]
    if not sorted_keys: return values
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    #if not sorted_keys: return values
    k = sorted_keys[0]
    
    for value in values[k]:
        values_copy = {k:v for (k,v) in values.items()}
        values_copy[k] = value
        vc = search(values_copy)
        if vc: return vc
    return False
            
            
    # If you're stuck, see the solution.py tab!