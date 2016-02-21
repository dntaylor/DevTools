#!/usr/bin/env python
import argparse
import logging
import sys

from DevTools.Analyzer.WZAnalysis import WZAnalysis

logger = logging.getLogger("WZAnalysis")
logging.basicConfig(level=logging.INFO, stream=sys.stderr)


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Run analyzer')

    parser.add_argument('--inputFiles', type=str, nargs='*', default=['/store/user/dntaylor/2016-02-19_DevTools_v1/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/2016-02-19_DevTools_v1/160219_162545/0000/miniTree_1.root'], help='Input files')
    parser.add_argument('--inputFileList', type=str, default='', help='Input file list')
    parser.add_argument('--outputFile', type=str, default='wzTree.root', help='Output file')

    return parser.parse_args(argv)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    wzAnalysis = WZAnalysis(
        outputFileName=args.outputFile,
        outputTreeName='WZTree',
        inputFileNames=args.inputFileList if args.inputFileList else args.inputFiles,
        inputTreeName='MiniTree',
        inputLumiName='LumiTree',
        inputTreeDirectory='miniTree',
    )
    
    try:
       wzAnalysis.analyze()
       wzAnalysis.finish()
    except KeyboardInterrupt:
       wzAnalysis.finish()

    return 0

if __name__ == "__main__":
    status = main()
    sys.exit(status)
