import sys

global_counter = 0

def work_print():
  global global_counter
  global_counter+=1
  if(global_counter%1000 == 0):
    sys.stdout.write('\b' * 100)
    sys.stdout.write("working %s ..." % global_counter)
    sys.stdout.write('\b' * 100)

