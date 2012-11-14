import os.path
from pprint import pprint
from src.solve import *
from src.parser import parse
from src.image.create_rep import create_rep
import src.visual.solve as visual
from src.meta_reasoning import meta

verbosity = 0 # Set from 0 to 2 inclusive.
              # VERBOSITY LEGEND:
              #
              # 0: just write the answer number
              # 1: motivate it's answer
              # 2: compare motivations between choices

show_both = True # Write solution for both methods or the most likely one?

def main():
  problems = ['2-1', '2-2', '2-3', '2-4', '2-5', '2-6', '2-7', '2-8',
              '3-7', '3-8',
              '4-7', '4-8']
  for x in problems:
    file_path = "reps/%s" % x
    if os.path.exists(file_path):
      image_tree = parse(file_path)
      d = meta(image_tree)
      print "+++++ ======================================================"
      print "The most likely answer based on both solvers is: \t%s" % d['ans']
      print ""
      print "Motivation: " + d['motivation']
      print ""
      if show_both:
        print "--------------------------------------------------------"
        print "Visual solution to problem %s is:" % (x)
        pprint(d['vis'][verbosity])
        print ""
        print "--------------------------------------------------------"
        print "Solution to problem %s is:" % (x)
        pprint(d['rep'][verbosity])
      else:
        print "The used solver gave this answer/solution:"
        pprint(d[d['used']][verbosity])
      print "============================================================"

      print "\n\n\n"
    else:
      print "Didn't find representation for file %s" % x

main()
