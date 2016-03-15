#!/usr/bin/env python
import argparse
import sys
import subprocess
import os

# import run script
from DevTools.Analyzer.runWZAnalysis import main as runWZ
from DevTools.Analyzer.runHpp3lAnalysis import main as runHpp3l
from DevTools.Analyzer.runHpp4lAnalysis import main as runHpp4l
from DevTools.Analyzer.runSingleElectronAnalysis import main as runSingleElectron
from DevTools.Analyzer.runSingleMuonAnalysis import main as runSingleMuon
from DevTools.Analyzer.runDijetFakeRateAnalysis import main as runDijetFakeRate
from DevTools.Analyzer.runElectronAnalysis import main as runElectron
from DevTools.Analyzer.runMuonAnalysis import main as runMuon

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Submit analyzers')

    parser.add_argument('analysis', type=str, choices=['WZ','Hpp3l','Hpp4l','SingleElectron','SingleMuon','Electron','Muon', 'DijetFakeRate'], help='Analysis to submit')

    return parser.parse_args(argv)



def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    # add on the input and output
    argv = ['--inputFileList',os.environ['INPUT'],'--outputFile',os.environ['OUTPUT']]

    # run the analyzer
    if args.analysis=='WZ':
        status = runWZ(argv)
    elif args.analysis=='Hpp3l':
        status = runHpp3l(argv)
    elif args.analysis=='Hpp4l':
        status = runHpp4l(argv)
    elif args.analysis=='SingleElectron':
        status = runSingleElectron(argv)
    elif args.analysis=='SingleMuon':
        status = runSingleMuon(argv)
    elif args.analysis=='DijetFakeRate':
        status = runDijetFakeRate(argv)
    elif args.analysis=='Electron':
        status = runElectron(argv)
    elif args.analysis=='Muon':
        status = runMuon(argv)
    else:
        status = 0

    return status

if __name__ == "__main__":
    status = main()
    sys.exit(status)
