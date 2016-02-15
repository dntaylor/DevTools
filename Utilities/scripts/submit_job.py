#!/usr/bin/env python

'''
submit_job.py

Script to submit jobs to crab or condor.
'''

import argparse
import logging
import os
import sys
from socket import gethostname

from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException


# i want to override this
#from CRABAPI.RawCommand import crabCommand

import CRABAPI
from CRABClient.ClientUtilities import initLoggers, flushMemoryLogger, removeLoggerHandlers

# NOTE: Not included in unittests
def crabCommand(command, *args, **kwargs):
    """ crabComand - executes a given command with certain arguments and returns
                     the raw result back from the client. Arguments are...
    """
    #Converting all arguments to a list. Adding '--' and '='
    arguments = []
    for key, val in kwargs.iteritems():
        if isinstance(val, bool):
            if val:
                arguments.append('--'+str(key))
        else:
            arguments.append('--'+str(key))
            arguments.append(val)
    arguments.extend(list(args))

    return execRaw(command, arguments)


# NOTE: Not included in unittests
def execRaw(command, args):
    """
        execRaw - executes a given command with certain arguments and returns
                  the raw result back from the client. args is a python list,
                  the same python list parsed by the optparse module
    """
    tblogger, logger, memhandler = initLoggers()
    tblogger.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    memhandler.setLevel(logging.INFO)

    try:
        mod = __import__('CRABClient.Commands.%s' % command, fromlist=command)
    except ImportError:
        raise CRABAPI.BadArgumentException( \
                                        'Could not find command "%s"' % command)

    try:
        cmdobj = getattr(mod, command)(logger, args)
        res = cmdobj()
    except SystemExit as se:
        # most likely an error from the OptionParser in Subcommand.
        # CRABClient #4283 should make this less ugly
        if se.code == 2:
            raise CRABAPI.BadArgumentException
    finally:
        flushMemoryLogger(tblogger, memhandler, logger.logfile)
        removeLoggerHandlers(tblogger)
        removeLoggerHandlers(logger)
    return res

log = logging.getLogger("submit_job")
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

def submit_crab(args):
    '''Create submission script for crab'''
    submit_strings = []

    uname = os.environ['USER']
    scratchDir = 'data' if 'uwlogin' in gethostname() else 'nfs_scratch'

    # crab config
    from CRABClient.UserUtilities import config

    config = config()
    
    config.General.workArea         = '/{0}/{1}/crab_projects'.format(scratchDir,uname)
    config.General.transferOutputs  = True
    
    config.JobType.pluginName       = 'Analysis'
    config.JobType.psetName         = args.cfg
    config.JobType.pyCfgParams      = args.cmsRunArgs
    config.JobType.sendPythonFolder = True
    
    config.Data.inputDBS            = args.inputDBS
    config.Data.splitting           = 'FileBased'
    config.Data.unitsPerJob         = 1
    #config.Data.splitting           = 'LumiBased'
    #config.Data.splitting           = 'EventAwareLumiBased'
    #config.Data.unitsPerJob         = 100000
    config.Data.outLFNDirBase       = '/store/user/{0}/{1}/'.format(uname,args.jobName)
    config.Data.publication         = args.publish
    config.Data.outputDatasetTag    = args.jobName
    if args.applyLumiMask:
        config.Data.lumiMask        = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/'\
                                      'Collisions15/13TeV/'\
                                      'Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt'

    config.Site.storageSite         = 'T2_US_Wisconsin'

    # crab command options
    command = 'submit'
    commandArgs = []
    if args.dryrun: commandArgs += ['--dryrun']

    # get samples
    sampleList = []
    if os.path.isfile(args.sampleList):
        with open(args.sampleList,'r') as f:
            sampleList = [line.strip() for line in f]
    else:
        log.error('Sample input list {0} does not exist.'.format(args.sampleList))

    # iterate over samples
    for sample in sampleList:
        _, primaryDataset, datasetTag, dataFormat = sample.split('/')
        config.General.requestName = '{0}_{1}_{2}_{3}'.format(primaryDataset[:20],datasetTag[:20],dataFormat[:10],args.jobName[:30])
        config.Data.inputDataset   = sample
        try:
            log.info("Submitting for input dataset {0}".format(sample))
            res = crabCommand(command, config = config, *commandArgs)
        except HTTPException as hte:
            log.info("Submission for input dataset {0} failed: {1}".format(sample, hte.headers))
        except ClientException as cle:
            log.info("Submission for input dataset {0} failed: {1}".format(sample, cle))


def submit_condor(args):
    '''Create submission script for condor'''
    submit_string = ''
    if args.outfile:
        with open(args.outfile,'w') as f:
            f.write('#!/bin/bash\n')
            f.write(submit_string)
        log.info('Wrote submit script to {0}'.format(args.outfile))
    else:
        sys.stdout.write(submit_string)

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Submit jobs to grid')

    # submission type
    subparsers = parser.add_subparsers(help='Submission mode')

    # crab
    parser_crab = subparsers.add_parser('crab', help='Submit jobs via crab')
    parser_crab.add_argument('jobName', type=str, help='Job Name for submission')
    parser_crab.add_argument('cfg', type=str, help='cmsRun config file')
    parser_crab.add_argument('cmsRunArgs', nargs='*', 
        help='VarParsing arguments passed to cmsRun'
    )

    parser_crab.add_argument('--sampleList', type=str,
        help='Text file list of DAS samples to submit, one per line'
    )

    parser_crab.add_argument('--applyLumiMask',action='store_true',
        help='Apply the latest golden json run lumimask to data'
    )

    parser_crab.add_argument('--inputDBS', type=str, default='global',
        choices=['global','phys01','phys02','phys03'], 
        help='DAS instance to search for input files'
    )

    parser_crab.add_argument('--publish', action='store_true', help='Publish output to DBS')

    parser_crab.add_argument('--dryrun', action='store_true', help='Do not submit jobs')

    parser_crab.set_defaults(submit=submit_crab)

    # condor
    parser_condor = subparsers.add_parser('condor', help='Submit jobs via condor')
    parser_condor.add_argument('jobName', type=str, help='Job Name for submission')
    parser_condor.add_argument('cfg', type=str, help='cmsRun config file')
    parser_condor.add_argument('cmsRunArgs', nargs='*', 
        help='VarParsing arguments passed to cmsRun'
    )

    parser_condor.add_argument('--sampleList', type=str, nargs=1,
        help='Text file list of DAS samples to submit, one per line'
    )

    parser_condor.add_argument('--applyLumiMask',action='store_true',
        help='Apply the latest golden json run lumimask to data'
    )

    parser_condor.add_argument('--inputDBS', type=str, default='global',
        choices=['global','phys01','phys02','phys03'], 
        help='DAS instance to search for input files'
    )

    parser_condor.add_argument('-o','--outfile',type=str,default='',
        help='Output file name to write submission commands'
    )

    parser_condor.set_defaults(submit=submit_condor)

    return parser.parse_args(argv)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    submit_string = args.submit(args)

if __name__ == "__main__":
    status = main()
    sys.exit(status)
