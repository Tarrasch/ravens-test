import os.path
from pprint import pprint
from src.solve import *
from src.parser import parse
from src.image.create_rep import create_rep
import src.visual.solve as visual

method = solve              # Uncomment to just write the answer number
method = solve_verbose      # Uncomment to motivate it's answer
method = solve_very_verbose # Uncomment to compare motivations between choices

visual_method = visual.solve              # Uncomment to just write the answer number
visual_method = visual.solve_verbose      # Uncomment to motivate it's answer
visual_method = visual.solve_very_verbose # Uncomment to compare motivations between choices

def main():
  # for x in range(7,9):
  for x in ['2-2']:
    file_path = "reps/%s" % x
    if os.path.exists(file_path):
      image_tree = parse(file_path)
      print "--------------------------------------------------------"
      print "Visual solution to problem %s is:" % (x)
      pprint(visual_method(image_tree))
      continue
      tree = create_rep(image_tree)
      pprint(tree) # Uncomment to see the intemediete representation
      ans = method(tree)
      print "--------------------------------------------------------"
      print "Solution to problem %s is:" % (x)
      pprint(ans)
      print "\n\n\n"
    else:
      print "Didn't find representation for file %s" % x

main()
