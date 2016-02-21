#!/usr/bin/env python
import argparse
import sys
import subprocess
import os

# import wz run script
from DevTools.Analyzer.runWZAnalysis import main as runWZ

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # add on the input and output
    argv = ['--inputFileList',os.environ['INPUT'],'--outputFile',os.environ['OUTPUT']]

    # run the analyzer
    status = runWZ(argv)

    return status

if __name__ == "__main__":
    status = main()
    sys.exit(status)
