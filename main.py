from pprint import pprint
from src.solve import solve_verbose
from src.parser import parse


tree = parse("6.yaml")

pprint(tree)
pprint(list(solve_verbose(tree)))
