import random as rand


class State:
    A = 0
    B = 1
    C = 2


class Cell:
    def __init__(self, value, prevIndex):
        self.value = value
        self.prevIndex = prevIndex


def main():
    # State types: A, B, C
    states = []
    # Observable types: A, C, G, T
    observables = []
    # Transition matrix 3x3
    transitionProb = [
        [0.80, 0.90, 1.00],
        [0.05, 0.95, 1.00],
        [0.09, 0.24, 1.00],
    ]
    transitionProbV = [
        [0.80, 0.10, 0.10],
        [0.05, 0.90, 0.05],
        [0.09, 0.15, 0.76]
    ]
    # Emission matrix 3x4
    emissionProb = [
        [0.25, 0.5, 0.75, 1.00],
        [0.30, 0.50, 0.75, 1.00],
        [0.25, 0.25, 0.75, 1.00],
    ]
    emissionProbV = [
        [0.25, 0.25, 0.25, 0.25],
        [0.30, 0.20, 0.25, 0.25],
        [0.125, 0.125, 0.25, 0.25],
    ]

    # Initial state and observable
    states.append(2)
    observables.append(0)

    # Get observables (make sure to store states)
    generateRandomStatesAndObservables(states, observables, emissionProb, transitionProb)

    logGeneratedLists(states, observables)

    path, probability = viterbi(observables, transitionProbV, emissionProbV)

    viterbiStates = [0]*len(path)

    for i in range(0, len(path)):
        viterbiStates[i] = path[len(path)-i-1][0]

    counter = 0
    for i in range(0, len(viterbiStates)):
        if viterbiStates[i] == states[i]:
            counter = counter + 1

    print("Path:", path)
    print("Probability:", probability)
    print("States found from Viterbi: ", viterbiStates)
    print("Original states: ", states)
    print("A:")
    print("Original states: ", states.count(0))
    print("Viterbi states: ", viterbiStates.count(0))
    print("B:")
    print("Original states: ", states.count(1))
    print("Viterbi states: ", viterbiStates.count(1))
    print("C:")
    print("Original states: ", states.count(2))
    print("Viterbi states: ", viterbiStates.count(2))
    print("Same values in same i count: ", counter)


def viterbi(observables, transitionProb, emissionProb):
    viterbiMatrix = [[Cell(0, [])] * len(observables) for i in range(3)]

    numCols = len(viterbiMatrix[0])
    numRows = len(viterbiMatrix)

    # Initialize first column (A is always first state)
    viterbiMatrix[0][0] = Cell(0, [0, 0])
    viterbiMatrix[1][0] = Cell(0, [0, 0])
    viterbiMatrix[2][0] = Cell(1, [0, 0])

    for j in range(1, numCols):
        for i in range(0, numRows):
            maxPrevCell = 0
            maxPrevCellIndex = []
            for k in range(0, numRows):
                # Find max v(k,j-1) for each k, and store in maxPrevCell + maxPrevCellIndex
                if viterbiMatrix[k][j-1].value * transitionProb[k][i] > maxPrevCell:
                    maxPrevCell = viterbiMatrix[k][j-1].value * transitionProb[k][i]
                    maxPrevCellIndex = [k, j-1]

            # Max found, multiply by emission
            maxPrevCell = maxPrevCell * emissionProb[i][observables[j]]

            viterbiMatrix[i][j] = Cell(maxPrevCell, maxPrevCellIndex)

    # Initiate max sequence path and probability
    maxSeqProb = -1
    i = 0
    maxSeqPath = [[-1]*2 for i in range(len(observables))]

    # Get max sequence probability and index
    for i in range(0, numRows):
        if viterbiMatrix[i][numCols-1].value > maxSeqProb:
            maxSeqProb = viterbiMatrix[i][numCols-1].value
            maxSeqPath[0] = [i, numCols-1]

    for i in range(0, numCols-1):
        if viterbiMatrix[maxSeqPath[i][0]][maxSeqPath[i][1]].prevIndex:
            maxSeqPath[i+1] = viterbiMatrix[maxSeqPath[i][0]][maxSeqPath[i][1]].prevIndex

    return maxSeqPath, maxSeqProb


def logGeneratedLists(states, observables):
    print("States: \n", states)
    print("Observables: \n", observables)


def generateRandomStatesAndObservables(states, observables, emissionProb, transitionProb):
    for x in range(1, 520):
        randNum = rand.random()
        prevState = states[x - 1]

        i = 0
        if prevState == State.A:
            # Get current state
            while transitionProb[State.A][i] < randNum:
                i = i + 1
            states.append(i)  # Push first state that fit from transition probability table

            i = 0
            # Get current observable
            while emissionProb[State.A][i] < randNum:
                i = i + 1
            observables.append(i)  # Push first observable that fit from emission probability table

        elif prevState == State.B:
            # Get current state
            while transitionProb[State.B][i] < randNum:
                i = i + 1
            states.append(i)

            i = 0
            while emissionProb[State.B][i] < randNum:
                i = i + 1
            observables.append(i)

        elif prevState == State.C:
            # Get current state
            while transitionProb[State.C][i] < randNum:
                i = i + 1
            states.append(i)

            i = 0
            while emissionProb[State.C][i] < randNum:
                i = i + 1
            observables.append(i)


if __name__ == '__main__':
    main()
