import getopt
import sys

opts, args = getopt.getopt(sys.argv[1:], '', ['to='])

print(opts)
print(args)