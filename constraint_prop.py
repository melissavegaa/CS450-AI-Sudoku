'''
Constraint propagation
'''

def AC3(csp, queue=None, removals=None):
    """AC3 constraint propagation

    csp - constraint satisfaction problem
    queue - list of constraints (might be None in which case they are
        populated from csp's variable list (len m) and neighbors (len k1...km):
        [(v1, n1), (v1, n2), ..., (v1, nk1), (v2, n1), (v2, n3), ... (v2, nk2),
         (vm, n1), (vk, n2), ..., (vk, nkm) ]
    removals - List of variables and values that have been pruned.  This is only
        useful for backtracking search which will enable us to restore things
        to a former point

    returns
        True - All constraints have been propagated and hold
        False - A variables domain has been reduced to the empty set through
            constraint propagation.  The problem cannot be solved from the
            current configuration of the csp.
    """

    # Hints:
    # Remember that:
    #    csp.variables is a list of variables
    #    csp.neighbors[x] is the neighbors of variable x
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.curr_domains for Xk in csp.neighbors[Xi]]  # Binary arcs in CSP

    while queue:
        (Xi, Xj) = queue.pop()  # Get binary constraint
        if revise(csp, Xi, Xj, removals):
            if csp.domains[Xi] is None:
                return False
            else:
                for Xk in csp.neighbors[Xi]:
                    if (Xk, Xi) not in queue:
                        queue.append((Xk, Xi))
    return True

def revise(csp, Xi, Xj, removals):
    """Return true if we remove a value.
    Given a pair of variables Xi, Xj, check for each value i in Xi's domain
    if there is some value j in Xj's domain that does not violate the
    constraints.

    csp - constraint satisfaction problem
    Xi, Xj - Variable pair to check
    removals - list of removed (variable, value) pairs.  When value i is
        pruned from Xi, the constraint satisfaction problem needs to know
        about it and possibly updated the removed list (if we are maintaining
        one)
    """
    revised = False
    # Restrict the domain Xi so that it is consistent with the domain Xj
    for x in csp.curr_domains[Xi]:
        # if not ∃y∈domain(Xj) such that constraint holds between x & y, prune Xi = x
        if not any([csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]]):
            csp.prune(Xi, x, removals)  # Delete x from domain(Xi)
            revised = True
    return revised


