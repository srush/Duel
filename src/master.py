import sys
import operator      
from subproblem import *
class DualMaster(object):
  """Controller for managing a DualDecomposition.

  tagging_master = Master([prob1, prob2] ,
                          MasterConfig()) 
  """
  class Config(object):
    """Record class for data that needs to be included in Master"""
    def __init__(self,
               max_iterations = 40,
               rate = None):
      self.max_iterations = max_iterations
      self.rate = rate
      
  def __init__(self, subproblems, config, log = (lambda a:Nothing)):
    self.config = config
    self.subproblems = subproblems
    self.penalty_weights = [{}] * len(subproblems)

    # current iteration of the algorithm
    self.iteration = 0
    self.log = log
    self.has_converged = False
    self.results = {}
    
  def current_results(self):
    return self.results[self.iteration -1]

  def objectives(self):
    return [sum([res.objective for res in subres]) for subres in self.results.itervalues()]
  
  def current_objective(self):
    return sum([res.objective for res in self.current_results()])

  def run(self):
    while not self.has_converged \
          and self.iteration < self.config.max_iterations:
      self._run_one_step()


  def _log_state(self):
    self.log("Iteration %s"%self.iteration)
    res =  self.current_results()
    for r in res:
      r.log_result(self.log)
    #self.log("Disagree: %s" % (res[0].assignment.keys^ res[1].assignment))
    self.log("Combined Objective %s"% self.current_objective())
    if self.last_alpha:
      self.log("Last alpha %s"% self.last_alpha)
    self.log("\n")
    self.log("New Weights %s"%self.penalty_weights)

  @classmethod
  def _compute_penalty_weights(_, cur_result, results):
    theta = {}
    for d in cur_result.assignment:
      for assignment in cur_result.assignment[d]:
        theta.setdefault((d,assignment), 0.0)
        theta[d,assignment] -= 1.0


    for res in results:
      if res is cur_result: continue
      for d in res.subproblem.domains:
        if res.assignment.has_key(d):
          for assignment in res.assignment[d]:
            theta.setdefault((d,assignment), 0.0)
            theta[(d,assignment)] += 1.0
    return theta 


  def _update_penalty_weights(self, results):
    alpha = self.config.rate.computeAlpha(self.objectives())
    self.last_alpha = alpha
    for i in xrange(len(results)):
      new_weights = DualMaster._compute_penalty_weights(results[i],results)
      scaled = scale_dict(new_weights, alpha) 
      self.penalty_weights[i] = add_dict(self.penalty_weights[i], scaled) 

  def _check_convergence(self, results):
    for subres in results:
      for domain in subres.subproblem.domains:
        for subres2 in results:
          if domain in subres2.subproblem.domains:
            if subres2.assignment[domain] <> subres.assignment[domain]:
              return False
    return True


  def _run_one_step(self):
    """
    k
    """
    # run subproblems
    results = []
    for i in range(len(self.subproblems)):
      results.append(self.subproblems[i].solve(self.penalty_weights[i]))
    
    self.results[self.iteration] = results
    # update master
    self._update_penalty_weights(results)
    self.has_converged = self._check_convergence(results)
    self.iteration += 1
    self._log_state()


    
class LearningRate:
  def __init__(self, alpha = 0.5, max_counts = 10):
    self.cur_alpha = alpha
    self.counter = 0
    self.max_counts =max_counts
  def computeAlpha(self, objective):
    is_looping = self.counter > 2 and \
                objective[-1] == objective[-3]
      
    self.counter += 1
    
    if is_looping \
       or self.counter > self.max_counts :
      self.cur_alpha /= 2
      self.counter = 0
    return self.cur_alpha
       


def add_dict(a, b):
  return dict( (n, a.get(n, 0)+b.get(n, 0)) for n in set(a.keys())|set(b.keys()) )

  
def log_stdout(s):
  print s
