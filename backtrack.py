

from csp_lib.backtrack_util import (first_unassigned_variable, 
                                    unordered_domain_values,
                                    no_inference)

def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference,
                        verbose=False):
    """backtracking_search
    Given a constraint satisfaction problem (CSP),
    a function handle for selecting variables, 
    a function handle for selecting elements of a domain,
    and a function handle for making inferences after assignment,
    solve the CSP using backtrack search

    If verbose is True, prints number of assignments and inferences

    Returns two outputs:
       dictionary of assignments or None if there is no solution
       Number of variable assignments made in backtrack search (not counting
       assignments made by inference)
    """

    # See Figure 6.5 of your book for details
    def backtrack(assignment: dict):
        """
        Search for a consistent assignment for the constraint satisfaction problem
        """

        # Check if assignment is complete
        # If complete, return a dictionary of current domains
        complete = 81
        if len(assignment) == complete:
            return dict(csp.curr_domains)

        var = select_unassigned_variable(assignment, csp)  # Select next unassigned variable
        for value in order_domain_values(var, assignment, csp):
            if csp.nconflicts(var, value, assignment) == 0:  # Check if value is consistent with assignment
                csp.assign(var, value, assignment)  # Add {var: value} to assignment

            # Propagate new constraints so that search works faster
                removals = list()  # Create a list of removals
                inferences = inference(csp, var, value, assignment, removals)
                # If inferences are found, determine a temporary assignment
                if inferences:
                    removals = removals + csp.suppose(var, value)  # Return a list of removals
                    result = backtrack(assignment)

                    # If result does not equal failure, return result
                    if result is not None:
                        return result

                    # Inconsistent value of further exploration failed
                    # Restore assignments to its state at top of loop and try next value
                    csp.restore(removals)
                    csp.unassign(var, assignment)

        # No value was consistent with the constraints
        return None

    # Empty call with no assignments
    final_result = backtrack({})
    # If valid solution is found, return final result
    # If no solution is found, return final result
    assert final_result is None or csp.goal_test(final_result)
    return final_result
