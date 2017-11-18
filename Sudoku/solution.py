assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

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
    # Eliminate the naked twins as possibilities for their peers
    two_list = []
    unit_dict = {}
    
    #Find all box's values length is two,and putting the box into two_list.
    for key,value in values.items():
        if len(value) == 2 :
            two_list.append(key)
        else:
            continue

    #Find all boxes more than one value in one unit,which having the same value.
    #Create unit_dict ,which the box as key and the list to be eliminate as value .
    for box,unit in units.items():
        if box in two_list:
            for i in [j for j in two_list if j != box] :
                if i in unit[0] and values[box] == values[i]:
                    unit_dict[tuple([k for k in unit[0] if k != box and k != i ])] = (i,box)
                if i in unit[1] and values[box] == values[i]:
                    unit_dict[tuple([k for k in unit[1] if k != box and k != i ])] = (i,box)
                if i in unit[2] and values[box] == values[i]:
                    unit_dict[tuple([k for k in unit[2] if k != box and k != i ])] = (i,box)
                else:
                    continue
        else:
            continue

    #If the naked_twins is not exist,return the values.
    if not unit_dict:
        return values

    #Eliminate the naked twins value from the left unit(s).
    for key,value in unit_dict.items():
        for box in key:
            if len(values[value[0]]) == 2 and len(values[value[1]]) == 2:
                assign_value(values,box,values[box].replace(values[value[0]][0],'').replace(values[value[0]][1],''))
            else:
                naked_twins(values)

    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [i+j for i in A for j in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
diag_box = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],['A9','B8','C7','D6','E5','F4','G3','H2','I1']]


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
    boxes = cross('ABCDEFGHI','123456789')
    values = dict(zip(boxes,list(grid)))
    for box,value in values.items():
        if value == '.':
            assign_value(values,box,'123456789')
        else:
            continue
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    boxes = cross('ABCDEFGHI','123456789')
    for box in boxes:
        if box == 'D1' or box == 'G1':
            print('---+---+---')
        print(values[box],end='')
        if int(box[1]) % 3 == 0 and box[1] != '9':
            print('|',end='')
        if box[1] == '9':
            print('')


def eliminate(values):
    #Make sure the values is correct style.
    assert len(values) == 81
    
    for key,value in values.items():

        if len(value) == 1 :
            #Box not in diagnal,just eliminating value from the box's peers.
            if key not in (diag_box[0] + diag_box[1]):
                for i in peers[key]:
                    assign_value(values,i,values[i].replace(value,''))
            #Box in one of diagnal,eliminating value from the box's peers and one of diagnal.
            elif key in diag_box[0]:
                new_diag_box_one = diag_box[0][:]
                new_diag_box_one.remove(key)
                all_eli_box = list(peers[key]) + new_diag_box_one
                    
                for i in all_eli_box:
                    assign_value(values,i,values[i].replace(value,''))
            #Box in another of diagnal,eliminating value from the box's peers and another of diagnal.
            elif key in diag_box[1]:
                new_diag_box_two = diag_box[1][:]
                new_diag_box_two.remove(key)
                all_eli_box = list(peers[key]) + new_diag_box_two

                for i in all_eli_box:
                    assign_value(values,i,values[i].replace(value,''))
        else:
            continue

    return values


def only_choice(values):
    assert len(values) == 81
    for box,unit in units.items():
        if len(values[box]) >1:
            for i in values[box]:
                #If box's one value not in one of unit except itself,assign the value to the box.
                if i not in set(''.join([values[j] for j in unit[0] if j != box])) \
                    or i not in set(''.join([values[j] for j in unit[1] if j != box])) \
                    or i not in set(''.join([values[j] for j in unit[2] if j != box])):
                        assign_value(values,box,i)
                else:
                    continue
        else:
            continue
    return values


def reduce_puzzle(values):
    assert len(values) == 81
    stalled = False
    
    while not stalled:
        #The number of  box's value length is one.
        reduce_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)

        #The number of  box's value length is one.
        reduce_after = len([box for box in dict(values).keys() if len(values[box]) == 1])
        #If the reduce_before equal reduce_after,stalled will be True.
        stalled = reduce_before == reduce_after
        #The box's value length less than 1,the function may be wrong.
        if len([box for box in values.keys() if len(values[box]) < 1]):
            return False
    return values


def search(values):
    assert len(dict(values)) == 81
    
    values = reduce_puzzle(values)
    if values == False:
        
        return False
    
    if all([len(values[box]) == 1 for box in values.keys()]):
        return values
    #Find value the shortest one,which box's value length longer than 1.
    n,s = min((len(values[box]),box) for box in values.keys() if len(values[box]) >1)

    for value in values[s]:
        new_values = values.copy()
        assign_value(new_values,s,value)
        attempt = search(new_values)
        if attempt:
            return attempt
        

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)

    values = search(values)
    if all([len(values[box])==1 for box in values.keys()]) :
        return values
    else:
        return False
    

if __name__ == '__main__':
    #diag_sudoku_grid = '......8.68.........7..863.....8............8..8.5.9...1.8..............8.....8.4.'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
