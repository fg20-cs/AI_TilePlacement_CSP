import sys
from CSP import CSP
from print import *

# getting file name from the command line
input_args = len(sys.argv)
if input_args < 2:
  exit()
file_name = sys.argv[-1]

csp = CSP()

# keep all the possible tile assignments in the list
functions = [csp.L_shape_1, csp.L_shape_2, csp.L_shape_3, csp.L_shape_4, csp.Full_block, csp.Outer_block]

# get all the data from the file
csp.extract_data_from_file(file_name)

solution = csp.csp_with_MRV(0, {1:0, 2:0, 3:0, 4:0}, functions)
if solution:
    print('\n')
    print("Target: ", end="")
    print(csp.bushes_target)
    print('\n')
    print("Final Path:")
    print(csp.path)
    print('\n')
    csp.apply_path_to_landscape()
    print_landscape_with_blocks(csp.landscape_areas)
else:
    print("No path found.")

print("")