#!/usr/bin/env python
import argparse
import logging
import sys

from DevTools.Analyzer.utilities import getTestFile
from DevTools.Analyzer.WZAnalysis import WZAnalysis

logger = logging.getLogger("WZAnalysis")
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Run analyzer')

    parser.add_argument('--inputFiles', type=str, nargs='*', default=[getTestFile('MC')], help='Input files')
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
