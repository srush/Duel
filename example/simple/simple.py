from master import *
from subproblem import *

class AlwaysOn(SubProblem):
  def name(self):
    return "Always On"
  def solve(self, penalty):
    return Result(self, set(["1"]), 0.0)

class Follower(SubProblem):
  def name(self):
    return "Follower"
  def solve(self, penalty):
    return Result(self, set(penalty.keys()), 0.0)

def main():
  master = DualMaster([AlwaysOn(), Follower()],DualMaster.Config(rate = LearningRate()), log_stdout)
  master.run()


if __name__=="__main__":
  main()
