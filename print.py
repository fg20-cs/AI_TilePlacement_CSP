import math

# function to print the landscape with the assigned blocks
def print_landscape_with_blocks(landscape):

  def get_matrices_side_by_side(areas):
    result = ""
    for i in range(4):
      temp = ""
      for area in areas:
        row_str = str(area[i]).strip("[]")
        row_str = row_str.replace(',', '')
        row_str = row_str.replace('-1', "\033[92m0\033[00m") # coloring the blocks in green
        temp = temp + row_str + "  "
      result = result + temp + "\n"
    return result
  
  rows = int(math.sqrt(len(landscape)))
  areas = ""
  for i in range(0, len(landscape), rows):
    r = get_matrices_side_by_side(landscape[i:i+rows])
    areas += r + "\n"
  print(areas)