class CSP:

  def __init__(self):
    self.path = []
    self.landscape_areas = []
    self.tiles = {}
    self.bushes_target = {}

  # func to extract all the required data from the file
  def extract_data_from_file(self, file_name):
    maze = []
    with open(file_name, 'r') as file:
    #getting the inital landscape
      for line in file:
        if "Landscape" in line:
          break
      else: raise ValueError(f"Not an appropriate file: you passed {file_name}")
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
          self.landscape_areas.append(area)

      # getting the number of tiles
      for line in file:
        if "Tiles" in line:
          break
      else: raise ValueError("Not an appropriate file")
      line = file.readline()
      line = line.strip("{}\n")
      line = line.split(", ")
      for pair in line:
        key, value = pair.split("=")
        self.tiles[key] = int(value)
      
      # getting the final count of bushes
      for line in file:
        if "Targets" in line:
          break
      else: raise ValueError("Not an appropriate file")
      for _ in range(4):
        bush = file.readline()
        bush = bush.strip()
        bush = bush.split(":")
        self.bushes_target[int(bush[0])] = int(bush[1])
  
  # fucntion to apply FULL_BLOCK to a 4x4 area
  # returns a dictionary with the count of visible bushes of each type
  def Full_block(self, area):
    return {1: 0, 2: 0, 3: 0, 4: 0}
  
  # fucntion to apply OUTER_BOUNDARY to a 4x4 area
  # returns a dictionary with the count of visible bushes of each type
  def Outer_block(self, area):
      res = {1: 0, 2: 0, 3: 0, 4: 0}
      res[1] = sum(row[1:3].count(1) for row in area[1:3])
      res[2] = sum(row[1:3].count(2) for row in area[1:3])
      res[3] = sum(row[1:3].count(3) for row in area[1:3])
      res[4] = sum(row[1:3].count(4) for row in area[1:3])
      return res
  
  # fucntion to apply EL_SHAPE of type 〡_ to a 4x4 area
  # returns a dictionary with the count of visible bushes of each type
  def L_shape_1(self, area):
    res = {1: 0, 2: 0, 3: 0, 4: 0}
    res[1] = sum(row[1:].count(1) for row in area[:-1])
    res[2] = sum(row[1:].count(2) for row in area[:-1])
    res[3] = sum(row[1:].count(3) for row in area[:-1])
    res[4] = sum(row[1:].count(4) for row in area[:-1])
    return res

  # fucntion to apply EL_SHAPE of type 〡﹉ to a 4x4 area
  # returns a dictionary with the count of visible bushes of each type
  def L_shape_2(self, area):
    res = {1: 0, 2: 0, 3: 0, 4: 0}
    res[1] = sum([row[1:].count(1) for row in area[1:]])
    res[2] = sum([row[1:].count(2) for row in area[1:]])
    res[3] = sum([row[1:].count(3) for row in area[1:]])
    res[4] = sum([row[1:].count(4) for row in area[1:]])
    return res
  
  # fucntion to apply EL_SHAPE of type _〡 to a 4x4 area
  # returns a dictionary with the count of visible bushes of each type
  def L_shape_3(self, area):
    res = {1: 0, 2: 0, 3: 0, 4: 0}
    res[1] = sum(row[:-1].count(1) for row in area[:-1])
    res[2] = sum(row[:-1].count(2) for row in area[:-1])
    res[3] = sum(row[:-1].count(3) for row in area[:-1])
    res[4] = sum(row[:-1].count(4) for row in area[:-1])
    return res
  
  # fucntion to apply EL_SHAPE of type 〡﹉ to a 4x4 area
  # returns a dictionary with the count of visible bushes of each type
  def L_shape_4(self, area): 
    res = {1: 0, 2: 0, 3: 0, 4: 0}
    res[1] = sum(row[:-1].count(1) for row in area[1:])
    res[2] = sum(row[:-1].count(2) for row in area[1:])
    res[3] = sum(row[:-1].count(3) for row in area[1:])
    res[4] = sum(row[:-1].count(4) for row in area[1:])
    return res
  
  # function to apply a given tile to a 4x4 area
  # returns a dictionary with the count of visible bushes of each type
  def apply(self, func, area):
      return func(area)
  
  # function to check 3 constraints and if reached the goal state: 
  def check(self, current_state, path):

    #checking if the tile count is not exceeding the available number of tiles
    count_L = path.count('L_shape_1') + path.count('L_shape_2') + path.count('L_shape_3') + path.count('L_shape_4')
    count_full = path.count('Full_block')
    count_out = path.count('Outer_block')
    if (count_L > self.tiles['EL_SHAPE']) or (count_full > self.tiles['FULL_BLOCK']) or (count_out > self.tiles['OUTER_BOUNDARY']):
      return 'used too many tiles'

    #checking the difference between visible bushes in current state and the goal state
    dist = {key: self.bushes_target[key] - current_state[key] for key in self.bushes_target if key in current_state}
    goal = True
    for value in dist.values():
      if value != 0:
        goal = False
        break
    
    # reached the goal state
    if goal:
      return 'end'
    
    # uncovered too many bushes
    if min(dist.values()) < 0:
      return 'too many visible bushes'
      
    return None
  
  # recursive function that checks constraints and applies MRV heuristics
  # returns True if the path was found, False otherwise
  def csp_with_MRV(self, current_index, current_sum, functions):  

    # check if reached the final state
    if current_index == len(self.landscape_areas):
      if self.check(current_sum, self.path) == 'end':            
        return True
      else: return False
    
    #applying MRV heuristic
    else:
      all_functions = [f for f in functions]
      all_functions = sorted(all_functions, key=lambda f: len([v for v in f(self.landscape_areas[current_index]).values() if v > 0]))
      
      for func in all_functions:
        self.path.append(func.__name__)
        applied_area = self.apply(func, self.landscape_areas[current_index])
          
        current_bushes = {}
        for key in applied_area:
          if key in current_sum:
            current_bushes[key] = current_sum[key] + applied_area[key]
            
        # Check if any constraint is violated
        checks = self.check(current_bushes, self.path)
        if checks == 'too many visible bushes' or checks == 'used too many tiles':
          self.path.pop()
          continue
                          
        solution = self.csp_with_MRV(current_index + 1, current_bushes, functions)
                
        if solution: return True
        else: self.path.pop()

      return False
  
  # function to apply the found path to the landscape
  # returns the count of bushes revealed
  def apply_path_to_landscape(self):
  
    def reset_matrix():
      return [[-1 for _ in range(4)] for _ in range(4)]
      
    def copy_inner(matrix_source, matrix_dest, pattern):
      if pattern == "outer_block":
        rows, cols = slice(1, -1), slice(1, -1)
      elif pattern.startswith("L_shape"):
        if pattern == "L_shape_1":
          rows, cols = slice(None, -1), slice(1, None)
        elif pattern == "L_shape_2":
          rows, cols = slice(1, None), slice(1, None)
        elif pattern == "L_shape_3":
          rows, cols = slice(None, -1), slice(None, -1)
        elif pattern == "L_shape_4":
          rows, cols = slice(1, None), slice(None, -1)
        else:
          raise ValueError("Invalid L_shape pattern")
      else:
        raise ValueError("Invalid pattern")
    
      for r_dest, r_source in zip(matrix_dest[rows], matrix_source[rows]):
              r_dest[cols] = r_source[cols]

    def count_bushes():
      bushes = {1:0, 2:0, 3:0, 4:0}
      for area in self.landscape_areas:
        for row in area:
          bushes[1] += row.count(1)
          bushes[2] += row.count(2)
          bushes[3] += row.count(3)
          bushes[4] += row.count(4)
      return bushes

    for index, block_type in enumerate(self.path):
      temp = reset_matrix()
          
      if block_type == 'Full_block':
        self.landscape_areas[index] = temp
      elif block_type == 'Outer_block':
        copy_inner(self.landscape_areas[index], temp, "outer_block")
        self.landscape_areas[index] = temp
      elif block_type in ['L_shape_1', 'L_shape_2', 'L_shape_3', 'L_shape_4']:
        copy_inner(self.landscape_areas[index], temp, block_type)
        self.landscape_areas[index] = temp
      else:
        raise ValueError("Invalid block type")
      
    return count_bushes()