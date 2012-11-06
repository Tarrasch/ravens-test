def map_tree(f, tree):
  grid = tree['grid']
  alts = [tree[k] for k in range(100) if tree.has_key(k)]
  grid = map(lambda xs: map(lambda x: f(x), xs), grid)
  alts = map(lambda x: f(x), alts)
  return dict([('grid', grid)] + [(i, alts[i-1]) for i in range(1,len(alts)+1)])

def collapse_tree(tree):
  grid = tree['grid']
  alts = [tree[k] for k in range(100) if tree.has_key(k)]
  return sum(sum(grid, []) + alts, [])
