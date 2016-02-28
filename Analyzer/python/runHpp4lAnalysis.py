#!/usr/bin/env python
import argparse
import logging
import sys

from DevTools.Analyzer.Hpp4lAnalysis import Hpp4lAnalysis

logger = logging.getLogger("Hpp4lAnalysis")
logging.basicConfig(level=logging.INFO, stream=sys.stderr)


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Run analyzer')

    parser.add_argument('--inputFiles', type=str, nargs='*', default=['/store/user/dntaylor/2016-02-27_DevTools_v1/HPlusPlusHMinusMinusHTo4L_M-500_13TeV-pythia8/2016-02-27_DevTools_v1/160227_142623/0000/miniTree_1.root'], help='Input files')
    parser.add_argument('--inputFileList', type=str, default='', help='Input file list')
    parser.add_argument('--outputFile', type=str, default='hpp4lTree.root', help='Output file')

    return parser.parse_args(argv)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    hpp4lAnalysis = Hpp4lAnalysis(
        outputFileName=args.outputFile,
        outputTreeName='Hpp4lTree',
        inputFileNames=args.inputFileList if args.inputFileList else args.inputFiles,
        inputTreeName='MiniTree',
        inputLumiName='LumiTree',
        inputTreeDirectory='miniTree',
    )
    
    try:
       hpp4lAnalysis.analyze()
       hpp4lAnalysis.finish()
    except KeyboardInterrupt:
       hpp4lAnalysis.finish()

    return 0

if __name__ == "__main__":
    status = main()
    sys.exit(status)
