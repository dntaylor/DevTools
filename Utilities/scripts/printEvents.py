#!/usr/bin/env python

import os
import sys
import glob
import argparse
import logging

import ROOT

def print_detailed_wz(rtrow):
    print '{0}:{1}:{2}'.format(rtrow.run, rtrow.lumi, rtrow.event)
    print '    Triggers:'
    for trigger in [
        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
        'Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ',
        'Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
        'Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL',
        'Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
        'IsoMu20',
        'IsoTkMu20',
        'IsoMu27',
        'Ele23_WPLoose_Gsf',
        ]:
        print '        {0} {1}'.format(getattr(rtrow,'pass{0}'.format(trigger)),trigger)


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description="Print events from ntuple")

    parser.add_argument('files', nargs='+', help='File names w/ UNIX wildcards')
    parser.add_argument('-t','--tree',type=str,default='MiniTree',help='Tree name')
    parser.add_argument('-c','--cut',nargs='?',type=str,default='',help='Cut to be applied to tree')
    parser.add_argument('-e','--events',nargs='*',type=str,default=[],help='Events to print (form: run:lumi:event, space delimited)')
    parser.add_argument('-d','--detailed',action='store_true',help='Print detailed event information')
    parser.add_argument('--log',nargs='?',type=str,const='INFO',default='INFO',choices=['INFO','DEBUG','WARNING','ERROR','CRITICAL'],help='Log level for logger')
    args = parser.parse_args(argv)

    return args



def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    loglevel = getattr(logging,args.log)
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', level=loglevel, datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stderr)

    files = [filename for string in args.files for filename in glob.glob(string)]

    tchain = ROOT.TChain(args.tree)
    for f in files:
        tchain.Add(f)

    selectedEvents = tchain.CopyTree(args.cut) if args.cut else tchain

    rtrow = selectedEvents
    for r in xrange(rtrow.GetEntries()):
        rtrow.GetEntry(r)
        eventkey = '{0}:{1}:{2}'.format(rtrow.run, rtrow.lumi, rtrow.event)
        if args.events and eventkey not in args.events: continue
        if args.detailed:
            print_detailed_wz(rtrow)
        else:
            print eventkey

if __name__ == "__main__":
    main()
