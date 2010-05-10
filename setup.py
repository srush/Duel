import distutils.core
import sys


distutils.core.setup(
  name="duel",
  version="0.1",
  packages = ["duel", "duel_external"],
  package_dir = {"duel": "src/",
                 "duel_external": "thrift/gen-py/duel_external"},
  author="Sasha Rush",
  author_email="srush@mit.edu",
  url="http://srush.github.org/Duel/",
  license="http://www.apache.org/licenses/LICENSE-2.0",
  description=""
  )
                
