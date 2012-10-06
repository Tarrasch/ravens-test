import yaml

def parse(path):
  stream = open(path, 'r')
  return (yaml.load(stream))
