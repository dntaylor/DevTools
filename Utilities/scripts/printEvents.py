#!/usr/bin/env python

import os
import sys
import glob
import argparse
import logging

import ROOT


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description="Print events from ntuple (FSA or DBLH)")

    parser.add_argument('files', nargs='+', help='File names w/ UNIX wildcards')
    parser.add_argument('-c','--cut',nargs='?',type=str,default='',help='Cut to be applied to tree')
    parser.add_argument('--log',nargs='?',type=str,const='INFO',default='INFO',choices=['INFO','DEBUG','WARNING','ERROR','CRITICAL'],help='Log level for logger')
    args = parser.parse_args(argv)

    return args


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    loglevel = getattr(logging,args.log)
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', level=loglevel, datefmt='%Y-%m-%d %H:%M:%S')

    files = [filename for string in args.files for filename in glob.glob(string)]

    treeName = 'WZTree'
    tchain = ROOT.TChain(treeName)
    for f in files:
        tchain.Add(f)

    selectedEvents = tchain.CopyTree(args.cut) if args.cut else tchain

    rtrow = selectedEvents
    for r in xrange(rtrow.GetEntries()):
        rtrow.GetEntry(r)
        print '{0}:{1}:{2}'.format(rtrow.run, rtrow.lumi, rtrow.event)

if __name__ == "__main__":
    main()
