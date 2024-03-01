import math

# fucntion to apply the found path to the landscape
def apply_path_to_landscape(landscape, path):
  
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

  for index, block_type in enumerate(path):
    temp = reset_matrix()
        
    if block_type == 'Full_block':
      landscape[index] = temp
    elif block_type == 'Outer_block':
      copy_inner(landscape[index], temp, "outer_block")
      landscape[index] = temp
    elif block_type in ['L_shape_1', 'L_shape_2', 'L_shape_3', 'L_shape_4']:
      copy_inner(landscape[index], temp, block_type)
      landscape[index] = temp
    else:
      raise ValueError("Invalid block type")


# function to print the landscape with the assigned blocks
def print_landscape_with_blocks(landscape):

  def get_matrices_side_by_side(areas):
    result = ""
    for i in range(4):
      temp = ""
      for area in areas:
        row_str = str(area[i]).strip("[]")
        row_str = row_str.replace(',', '')
        row_str = row_str.replace('-1', "\033[92m0\033[00m")
        temp = temp + row_str + "  "
      result = result + temp + "\n"
    return result
  
  rows = int(math.sqrt(len(landscape)))
  areas = ""
  for i in range(0, len(landscape), rows):
    r = get_matrices_side_by_side(landscape[i:i+rows])
    areas += r + "\n"
  print(areas)