import yaml
from pprint import pprint
from src.solve import solve_verbose


stream = open("5.yaml", 'r')
tree = yaml.load(stream)

pprint(tree)
pprint(list(solve_verbose(tree)))
