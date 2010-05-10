from duel_external import Subsolver
from duel_external.ttypes import *
from duel.subproblem import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class ThriftSubproblem(Subproblem):
  def __init__(self, host, port):
    self.host = host
    self.port = port 
    self.transport = TSocket.TSocket(host, port)
    self.transport = TTransport.TBufferedTransport(self.transport)
    protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Subsolver.Client(protocol)

  def initialize(self, prob_data):  
    
    self.transport.open()
    solve_info  = self.client.initialize(prob_data)
    self.name = solve_info.name
    self.domains = solve_info.domains
    self.transport.close()
    
  def solve_internal(self, penalty):
    send_penalty = {}
    for (d,as) in penalty:
      send_penalty[as] = penalty[d,as]

    self.transport.open()
    subresult = self.client.solve_subproblem(send_penalty)
    self.transport.close()
    assignment = {}
    for assign in subresult.assignments:
      assignment.setdefault(assign.domain, [])
      assignment[assign.domain].append(assign.assign)
    return Result(self, assignment, subresult.score)


