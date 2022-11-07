import sys

# must have two arguments
if (len(sys.argv) < 3):
  print("Must be given two arguments")
  exit(1)

# get the input file and output directory
inputFile = sys.argv[1]
outputDir = sys.argv[2]

print("Input file: " + inputFile)
print("Output directory: " + outputDir)
exit(0)