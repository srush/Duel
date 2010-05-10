class Result(object):
  def __init__(self, subproblem, assignment, objective, result = None):
    self.objective = objective
    self.subproblem = subproblem
    self.assignment = assignment
  def log_result(self, log):
    log("""
      Subproblem Name %s
      Objective %s
      Assignment %s
      """% (self.subproblem.name, self.objective, self.assignment))

class Subproblem(object):
  def __init__(self):
    self.weighting = 1.0

  def solve(self, penalty):
    weighted_penalty = scale_dict(penalty, 1.0/self.weighting)
    
    result = self.solve_internal(weighted_penalty)
    result.objective *= self.weighting
    return result
  
  def solve_internal(self,penalty):
    pass

  
def scale_dict(d, val):
  return dict([(k,val * v) for (k,v) in d.iteritems()])
