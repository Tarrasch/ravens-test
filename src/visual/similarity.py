
def similarity(A, B):
  return 1.0*(A&B).sum()/(A|B).sum()
