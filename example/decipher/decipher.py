from duel.master import *
from duel.subproblem import *

from nltk.corpus import brown
from nltk.probability import LidstoneProbDist, WittenBellProbDist
from nltk.model.ngram import *
import math




class TrigramSubprob(Subproblem):
  def __init__(self, tri, lm):
    self.tri = tri
    self.name = "subprob" + str(tri)
    self.weighting = 1
    self.lm = lm
    self.domains = self.tri 

  def solve_internal(self, penalty):
    print "Solving %s"%self.name
    max_score = -100000
    max_tri = []
    for c1 in letters:
      if self.tri[0] == ' ' and c1 <> ord(' '):
        continue
      for c2 in letters:
        if self.tri[1] == ' ' and c2 <> ord(' '):
          continue

        for c3 in letters:
          if self.tri[2] == ' ' and c3 <> ord(' '):
            continue

          score = self.lm[c1, c2, c3] + \
                  penalty.get((str(self.tri[0]), chr(c1)), 0.0) +  \
                  penalty.get((str(self.tri[1]), chr(c2)), 0.0) + \
                  penalty.get((str(self.tri[2]), chr(c3)), 0.0)
          ok = True
          if score > max_score:
            if self.tri[0] == self.tri[1]:
              no = ok and (c1 == c2) 
            if self.tri[0] == self.tri[2]:
              no = ok and (c1 == c3) 
            if self.tri[1] == self.tri[2]:
              no = ok and (c2 == c3) 
            if ok:
              max_score = score
              max_tri = (chr(c1), chr(c2), chr(c3))
              
    return Result(self, [(str(self.tri[0]), str(max_tri[0])), (str(self.tri[1]), str(max_tri[1])), (str(self.tri[2]), str(max_tri[2]))], max_score)


class Decipher:
  def __init__(self, lm):
    self.lm = lm

  def decipher(self, sent):
    subprobs = [] 
    correct = 0.0
    for i in xrange(len(sent)-3):
      subprobs.append( TrigramSubprob(sent[i:i+3], self.lm))
      correct += self.lm[(ord(sent[i]),ord(sent[i+1]),ord(sent[i+2]))]
    print "Best score is : %s"%correct
    master = DualMaster(subprobs, DualMaster.Config(max_iterations = 400, rate = LearningRate()), log_stdout)
    master.run()

letters = range(ord('a'), ord('z')) + [ord(' ')]
def main():
  estimator = lambda fdist, bins: LidstoneProbDist(fdist, bins)
  #estimator = lambda fdist, bins: WittenBellProbDist(fdist, bins)
  lm = NgramModel(3, (" ".join(brown.words(categories='news'))), estimator)
  lm_cache = {} 
  for c1 in letters:
    for c2 in letters:
      for c3 in letters:
        p=  lm.prob(chr(c3), (chr(c1), chr(c2)))
        if p > 1.0 or p < 0.0:
          p = 1e-19
        lm_cache[c1, c2, c3] = math.log(p)
        
  #print lm_cache
  # print lm.logprob("a", ("b","c"))  
  master = Decipher(lm_cache)
  master.decipher("a fundamental source of knowledge in the world today is the book found in our libraries")


if __name__=="__main__":
  main()
