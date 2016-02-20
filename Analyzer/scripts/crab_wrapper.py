#!/usr/bin/env python
import argparse
import sys
import subprocess

# import wz run script
from DevTools.Analyzer.runWZAnalysis import main as runWZ

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # import the crab generated PSet.py
    import PSet
    fileList = list(PSet.process.source.fileNames)

    # add on the inputfiles
    argv += ['--inputFiles'] + fileList

    argv = argv[1:]
    print argv

    # run the analyzer
    status = runWZ(argv)
    print status

    # and generate the job report xml
    command = 'cmsRun -j FrameworkJobReport.xml -p PSet.py'
    out = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    print out

    return status

if __name__ == "__main__":
    status = main()
    sys.exit(status)
