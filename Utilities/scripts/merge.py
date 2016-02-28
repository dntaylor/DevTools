#!/usr/bin/env python
'''
Script to merge files.
'''
import argparse
import glob
import os
import sys

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Merge files from directory')

    parser.add_argument('directory',type=str,help='Input top-level directory to merge, merges each subdirectory into a single file.')
    parser.add_argument('destination',type=str,help='Destination directory to merge files into.')

    args = parser.parse_args(argv)

    return args


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    os.system('mkdir -p {0}'.format(args.destination))

    for directory in glob.glob('{0}/*'.format(args.directory)):
        if not os.path.isdir(directory): continue
        destname = os.path.basename(os.path.normpath(directory))
        destfile = '{0}/{1}.root'.format(args.destination,destname)
        sourcefiles = '{0}/*.root'.format(directory)
        command = 'hadd -f {0} {1}'.format(destfile,sourcefiles)
        os.system(command)
    

if __name__ == "__main__":
    status = main()
    sys.exit(status)

