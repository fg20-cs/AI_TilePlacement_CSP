import sys

#getting file name from the command line
input_args = len(sys.argv)
if input_args < 2:
  exit()
file_name = sys.argv[-1]

#func to extract all the required data from the file
def extract_data_from_file(file_name, landscape_areas, tiles, bushes_target):
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
    for i in range(0, len(maze), 4):
      for j in range(0, len(maze[0]), 4):
        area = [row[j:j+4] for row in maze[i:i+4]]
        landscape_areas.append(area)

    #getting the number of tiles
    for line in file:
      if "Tiles" in line:
        break
    line = file.readline()
    line = line.strip("{}\n")
    line = line.split(", ")
    for pair in line:
      key, value = pair.split("=")
      tiles[key] = int(value)
    
    #getting the final count of bushes
    for line in file:
      if "Targets" in line:
        break
    for _ in range(4):
      bush = file.readline()
      bush = bush.strip()
      bush = bush.split(":")
      bushes_target[int(bush[0])] = int(bush[1])


landscape_areas = []
tiles = {} 
bushes_target = {}

extract_data_from_file(file_name, landscape_areas, tiles, bushes_target)

