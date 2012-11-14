from pprint import pprint
from src.solve import *
from src.parser import parse
from src.image.create_rep import create_rep
import src.visual.solve as visual

# This module is simply selecting if to choose the visual or the representational answer.
def meta(image_tree):
  tree = create_rep(image_tree)
  vis_solution = visual.solve(image_tree)
  rep_solution = solve(tree)
  vis_answer = vis_solution[0]
  rep_answer = rep_solution[0]
  vis_score = vis_solution[1][0] # Note, these scores are of different dimensinonalities
  rep_score = rep_solution[1][2]

  d = {
      'vis': vis_solution,
      'rep': rep_solution,
  }
  if(rep_score < 1000):
    d.update({
      'ans': rep_answer,
      'used': 'rep',
      'motivation': "The represenational solver seemed quite confident in it's answer, so lets trust it",
    })
  else:
    d.update({
      'ans': vis_answer,
      'used': 'vis',
      'motivation': "The represenational solver didn't find anything likely, lets go with the visual answer",
    })

  return d

