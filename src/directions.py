from itertools import combinations

def lid_directionss():
  return combinations([(1, 0), (0, 1), (1, 1)], 2)

def direction_mnemonic(dir):
  return {
      (1, 0): "down",
      (0, 1): "right",
      (1, 1): "diag",
    }[dir]
