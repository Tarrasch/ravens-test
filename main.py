import os.path
from pprint import pprint
from src.solve import *
from src.parser import parse

method = solve              # Uncomment to just write the answer number
# method = solve_verbose      # Uncomment to motivate it's answer
# method = solve_very_verbose # Uncomment to compare motivations between choices


def main():
  for x in range(1,7):
    file_path = "reps/%s" % x
    if os.path.exists(file_path):
      tree = parse(file_path)
      # pprint(tree) # Uncomment to see the intemediete representation
      ans = method(tree)
      print "--------------------------------------------------------"
      print "Solution to problem %s is:" % (x)
      pprint(ans)
      print "\n\n\n"
    else:
      print "Didn't find representation for file %s" % x

main()
