import os.path
from pprint import pprint
from src.solve import *
from src.parser import parse

method = solve              # Uncomment to just write the answer number
method = solve_verbose      # Uncomment to motivate it's answer
method = solve_very_verbose # Uncomment to compare motivations between choices


def main():
  # for x in range(6,7):
  # for x in [1,2,3,4,5,6]:
  for x in [5]:
    file_path = "reps/%s" % x
    if os.path.exists(file_path):
      tree = parse(file_path)
      pprint(tree)
      ans = method(tree)
      # ans = 3
      print "--------------------------------------------------------"
      print "Solution to problem %s is:" % (x)
      pprint(ans)
      print "\n\n\n"
    else:
      print "Didn't find representation for file %s" % x

main()
