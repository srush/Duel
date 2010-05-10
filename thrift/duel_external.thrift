namespace python duel_external


struct SolverInfo {
   1: string name,
   2: list <string> domains
}

struct Assignment {
  1: string domain,
  2: string assign
}

struct Subresult {
   1: double score,
   2: list <Assignment> assignments
}

service Subsolver {
    SolverInfo initialize(1: string initialization),
    Subresult solve_subproblem(1: map <string, double> penalty_weights)
}