import sys

#getting file name from the command line
input_args = len(sys.argv)
if input_args < 2:
  exit()
file_name = sys.argv[-1]


class Landscape:

  def __init__(self, maze):
    self.maze = maze

class State:

  def __init__(self):
    pass

bushes_count = dict()
maze = []

with open(file_name, 'r') as file:
  
  #getting the inital landscape
  for line in file:
    if "Landscape" in line:
      break
  line_count = 0
  for line in file:
    line_count += 1
    ls = list(line)[:-1]
    ls = list(map(lambda x: x.replace(' ', '0'), ls))
    ls = list(map(lambda x: int(x), ls))
    ls = [ele for idx, ele in enumerate(ls) if idx%2 == 0]
    maze.append(ls)
    if line_count > len(ls)-1:
      break
  
  #getting the number of tiles
  for line in file:
    if "Tiles" in line:
      break
  tiles = file.readline()
  tiles = tiles.strip("{}\n")
  tiles = tiles.split(", ")
  tiles = {key: int(value) for key, value in (pair.split("=") for pair in tiles)}

  #getting the final count of bushes
  for line in file:
    if "Targets" in line:
      break

  bushes_final = {}
  for _ in range(4):
    bush = file.readline()
    bush = bush.strip()
    bush = bush.split(":")
    bushes_final[int(bush[0])] = int(bush[1])
