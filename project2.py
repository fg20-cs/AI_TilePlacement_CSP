import sys

input_args = len(sys.argv)

if input_args < 2:
  exit()

file_name = sys.argv[-1]

bushes_count = dict()

with open(file_name, 'r') as file:
  for line in file:
    if line == "# Landscape":
      break


