import yaml
from pprint import pprint
from src.solve import solve_verbose


stream = open("1.yaml", 'r')
tree = yaml.load(stream)

pprint(tree)
pprint(solve_verbose(tree))
