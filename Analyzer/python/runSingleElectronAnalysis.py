#!/usr/bin/env python
import argparse
import logging
import sys

from DevTools.Analyzer.SingleElectronAnalysis import SingleElectronAnalysis

logger = logging.getLogger("SingleElectronAnalysis")
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Run analyzer')

    parser.add_argument('--inputFiles', type=str, nargs='*', default=['/store/user/dntaylor/2016-02-27_DevTools_v1/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/2016-02-27_DevTools_v1/160227_142430/0000/miniTree_1.root'], help='Input files')
    parser.add_argument('--inputFileList', type=str, default='', help='Input file list')
    parser.add_argument('--outputFile', type=str, default='eTree.root', help='Output file')

    return parser.parse_args(argv)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    eAnalysis = SingleElectronAnalysis(
        outputFileName=args.outputFile,
        outputTreeName='ETree',
        inputFileNames=args.inputFileList if args.inputFileList else args.inputFiles,
        inputTreeName='MiniTree',
        inputLumiName='LumiTree',
        inputTreeDirectory='miniTree',
    )
    
    try:
       eAnalysis.analyze()
       eAnalysis.finish()
    except KeyboardInterrupt:
       eAnalysis.finish()

    return 0

if __name__ == "__main__":
    status = main()
    sys.exit(status)
