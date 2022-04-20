import numpy as np
import Binairo
import State
from Binairo import *


def FORWARD_CHECKING(state, cell):

    unassigned=[]
    for c in state.board[cell.x]:
        if c.value == '_':
            unassigned.append(c)
    col = np.array(state.board).transpose()
    for c in col[cell.y]:
        if c.value == '_':
            unassigned.append(c)
    passQueue = unassigned.copy()
    while len(unassigned) > 0:
        c = unassigned.pop(0)
        count = 0
        blockedValues = []
        for value in c.domain:
            c.value = value
            if not Binairo.is_consistent(state):
                blockedValues.append(value)
                count += 1
        c.value = '_'
        if count == 1:
            if blockedValues[0] == 'b':
                c.value = 'w'
            if blockedValues[0] == 'w':
                c.value = 'b'
        if count == 2:
            return False
    return True
    if AC3(state, passQueue):
        return True
    else:
        return False

def MRV(state):

    variable = None
    for i in range(state.size):
        for j in range(state.size):
            cell = state.board[i][j]
            if cell.value == '_' and len(cell.domain) == 1:
                variable = deepcopy(cell)
                break
    if variable is None:
        i, j = state.first_unassigned_index()
        variable = deepcopy(state.board[i][j])

    return variable

    return None
def LCV(state):
    variable = None
    if len(variable.domain) == 1:
        domain = variable.domain[0]
        local_state = deepcopy(state)
        local_state.board[variable.x][variable.y].value = domain
        new_state = FORWARD_CHECKING(local_state, variable)
        if is_consistent(new_state):
            result = Upgraded_backtrack(new_state)
            if result is not None:
                return result

def AC3(state, queue):

    while len(queue) > 0:

        Checkvalue = queue.pop(-1)

        cellCheckCount = 0
        blockedValues = []
        for value in Checkvalue.domain:

            Checkvalue.value = value
            for c in queue:


                count = 0
                for v in c.domain:

                    c.value = v
                    if not Binairo.is_consistent(state):

                        count += 1
                if count == 2:

                    blockedValues.append(value)

                    cellCheckCount += 1
                    break
                if len(c.domain) == 1 and count == 1:
                    blockedValues.append(value)
                    cellCheckCount += 1
                    break
                if cellCheckCount == 2:

                    return False
                if cellCheckCount == 1 and len(Checkvalue.domain) == 1:

                    return False
        if cellCheckCount == 1:

            if blockedValues[0] == 'b':

                Checkvalue.value = 'w'

            if blockedValues[0] == 'w':

                Checkvalue.value = 'b'

        Checkvalue.value = '_'

    return True
