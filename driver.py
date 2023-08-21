"""
I promise that the attached assignment is my own work.
I recognize that should this not be the case, I will be subject to penalties as outlined in the course syllabus.
[Melissa  Vega]
"""
from csp_lib.sudoku import (Sudoku, easy1, harder1)
from constraint_prop import AC3
from csp_lib.backtrack_util import mrv, mac, lcv
from backtrack import backtracking_search


for puzzle in [easy1, harder1]:
    print("Initial Sudoku state:")
    s = Sudoku(puzzle)  # construct a Sudoku problem
    # solve as much as possible by AC3 then backtrack search if needed
    # using MRV and MAC
    s.display(s.infer_assignment())  # Display the initial state of Sudoku puzzle

    # Solve Sudoku using AC3
    AC3(s)
    print("Sudoku puzzle after AC3 algorithm:")  # Print puzzle after constraint propagation
    s.display(s.infer_assignment())

    # If AC3 failed, utilize backtracking to solve Sudoku puzzle
    if not s.goal_test(s.curr_domains):
        print("AC3 algorithm failed.")
        print("Running backtracking search...")
        backtrack_solution = backtracking_search(s, inference=mac, order_domain_values=lcv, select_unassigned_variable=mrv)
        if backtrack_solution:
            print("Sudoku puzzle after backtracking search:")
            s.display(s.infer_assignment())  # Print puzzle after being solved using backtracking
        else:
            print("Backtracking search failed. Current state:")  # Backtracking failed, print current state
            s.display(s.infer_assignment())

