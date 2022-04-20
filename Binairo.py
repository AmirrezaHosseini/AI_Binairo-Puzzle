from copy import deepcopy
import math

import numpy as np
import algorithm
import Cell

import State
        

def check_Adjancy_Limit(state: State):

    #check rows
    for i in range(0,state.size):
        for j in range(0,state.size-2):
            if(state.board[i][j].value.upper()==state.board[i][j+1].value.upper() and 
            state.board[i][j+1].value.upper()==state.board[i][j+2].value.upper() and
            state.board[i][j].value !='_'and 
            state.board[i][j+1].value !='_'and
            state.board[i][j+2].value !='_' ):
                
                return False
    #check cols
    for j in range(0,state.size): # cols
        for i in range(0,state.size-2): # rows
            if(state.board[i][j].value.upper()==state.board[i+1][j].value.upper() 
            and state.board[i+1][j].value.upper()==state.board[i+2][j].value.upper() 
            and state.board[i][j].value !='_'
            and state.board[i+1][j].value !='_'
            and state.board[i+2][j].value !='_' ):
               
                return False
    
    return True

def check_circles_limit(state:State): # returns false if number of white or black circles exceeds board_size/2
    #check in rows
    for i in range(0,state.size): # rows
        no_white_row=0
        no_black_row=0
        for j in range(0,state.size): # each col
            # if cell is black or white and it is not empty (!= '__')
            if (state.board[i][j].value.upper()=='W' and state.board[i][j].value != '_'): no_white_row+=1
            if (state.board[i][j].value.upper()=='B' and state.board[i][j].value != '_'): no_black_row+=1
        if no_white_row > state.size/2 or no_black_row > state.size/2:
            
            return False
        no_black_row=0
        no_white_row=0

    # check in cols
    for j in range(0,state.size):#cols
        no_white_col=0
        no_black_col=0
        for i in range(0,state.size): # each row
            # if cell is black or white and it is not empty (!= '__')
            if (state.board[i][j].value.upper()=='W' and state.board[i][j].value != '_'): no_white_col+=1
            if (state.board[i][j].value.upper()=='B' and state.board[i][j].value != '_'): no_black_col+=1
        if no_white_col > state.size/2 or no_black_col > state.size/2:
            
            return False
        no_black_col=0
        no_white_col=0
    
    return True

def is_unique(state:State): # checks if all rows are unique && checks if all cols are unique
    # check rows
    for i in range(0,state.size-1):
        for j in range(i+1,state.size):
            count = 0
            for k in range(0,state.size):
                if(state.board[i][k].value.upper()==state.board[j][k].value.upper()
                and state.board[i][k].value!='_'
                and state.board[j][k].value!='_'):
                    count+=1
            if count==state.size:
                
                return False
            count=0

    # check cols
    for j in range(0,state.size-1):
        for k in range(j+1,state.size):
            count_col =0 
            for i in range(0,state.size):
                 if(state.board[i][j].value.upper()==state.board[i][k].value.upper()
                 and state.board[i][j].value != '_'
                 and state.board[i][k].value != '_' ):
                    count_col+=1
            if count_col == state.size:
               
                return False
            count_col=0 
   
    return True

def is_assignment_complete(state:State): # check if all variables are assigned or not
    for i in range(0,state.size):
        for j in range(0,state.size):
            if(state.board[i][j].value == '_'): # exists a variable wich is not assigned (empty '_')
                
                return False
    return True
    
    return True
def backTrack(state:State):


    if is_assignment_complete(state):
        return state

    unassigned = []

    for i in range(0, state.size):
        for j in range(0, state.size):
            if (state.board[i][j].value == '_'):
                unassigned.append(state.board[i][j])
    init = unassigned[0]

    for d in init.domain:
        local_state = deepcopy(state)
        local_state.board[init.x][init.y].value = d
        if is_consistent(local_state):
            result = backTrack(local_state)
            if result is not None:
                return result
    return None


def is_consistent(state:State):
    
    return check_Adjancy_Limit(state) and check_circles_limit(state) and is_unique(state)

def check_termination(state):
    
    return is_consistent(state) and is_assignment_complete(state)

def Forward_Checking(state:State,cell):

    unassigned = []
    for row in state.board[cell.x]:
        if row.value == '_':
            unassigned.append(cell)
    transpose=np.array(state.board).transpose()
    for col in transpose[cell.y]:
        if col.value == '_':
            unassigned.append(col)
    passQueue = unassigned.copy()
    while len(unassigned) > 0:
        c = unassigned.pop(0)
        count = 0
        blocked = []
        for value in c.domain:
            c.value = value

            if not is_consistent(state):
                blocked.append(value)
                count += 1
        c.value = '_'
        if count == 1:
            if blocked[0] == 'b':
                c.value = 'w'
            if blocked[0] == 'w':
                c.value = 'b'
        if count == 2:
            return False
    if algorithm.AC3(state, passQueue):
        return True
    else:
        return False


def backTrack_Forward(state:State):
    if is_assignment_complete(state):
        state.print_board()
        return
    unassigned = []

    for row in reversed(state.board):
        for cell in reversed(row):
            if cell.value == '_':
                unassigned.append(cell)
        if len(unassigned) == 2:
            break
    init = unassigned.pop(0)

    for d in init.domain:
        init.value=d
        #local_state.board[init.x][init.y].value = d
        if is_consistent(state):
            local_state = deepcopy(state)
            if algorithm.FORWARD_CHECKING(local_state,local_state.board[init.x][init.y]):
                backTrack_Forward(local_state)


# backtrack  using mrv, lcv and forward checking
def Upgraded_backtrack(state):
    if is_assignment_complete(state):
        state.print_board()
        return

    unassigned = None

    # MRV
    unassigned=algorithm.MRV(state)

    # LCV

"""
    for domain in unassigned.domain:
        local_state = deepcopy(state)
        local_state.board[variable.x][variable.y].value = domain
        new_state = forward_checking(local_state, variable)
        if is_consistent(new_state):
            result = modified_backtrack(new_state)
            if result is not None:
                return result
    return None
"""
