from itertools import combinations

def std_directions():
  return [(1, 0), (0, 1), (1, 1)]

def lid_directionss():
  return combinations(std_directions(), 2)

def direction_mnemonic(dir):
  return {
      (1, 0): "down",
      (0, 1): "right",
      (1, 1): "diag",
    }[dir]
