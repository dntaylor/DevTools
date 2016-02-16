#!/usr/bin/env python

'''
submit_job.py

Script to submit jobs to crab or condor.
'''

import argparse
import logging
import os
import sys
import glob
from socket import gethostname

from CRABClient.ClientExceptions import ClientException
from CRABClient.ClientUtilities import initLoggers
from httplib import HTTPException
import CRABClient.Commands.submit as crabClientSubmit
import CRABClient.Commands.status as crabClientStatus
import CRABClient.Commands.resubmit as crabClientResubmit


log = logging.getLogger("submit_job")
logging.basicConfig(level=logging.INFO, stream=sys.stderr)


def get_crab_workArea(args):
    '''Get the job working area'''
    uname = os.environ['USER']
    scratchDir = 'data' if 'uwlogin' in gethostname() else 'nfs_scratch'
    return '/{0}/{1}/crab_projects/{2}'.format(scratchDir,uname,args.jobName)

def submit_crab(args):
    '''Create submission script for crab'''
    submit_strings = []

    uname = os.environ['USER']

    tblogger, logger, memhandler = initLoggers()
    tblogger.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    memhandler.setLevel(logging.INFO)

    # crab config
    from CRABClient.UserUtilities import config

    config = config()
    
    config.General.workArea         = get_crab_workArea(args)
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

    # get samples
    sampleList = []
    if os.path.isfile(args.sampleList):
        with open(args.sampleList,'r') as f:
            sampleList = [line.strip() for line in f]
    else:
        log.error('Sample input list {0} does not exist.'.format(args.sampleList))

    submitMap = {}
    # iterate over samples
    for sample in sampleList:
        _, primaryDataset, datasetTag, dataFormat = sample.split('/')
        config.General.requestName = '{0}'.format(primaryDataset)
        if dataFormat in ['MINIAOD','AOD','RAW']: # its data, also specify the aquisition period
            config.General.requestName += '_' + datasetTag
        # make it only 100 characters
        config.General.requestName = config.General.requestName[:99] # Warning: may not be unique now
        config.Data.inputDataset   = sample
        # submit the job
        submitArgs = ['--config',config]
        if args.dryrun: submitArgs += ['--dryrun']
        try:
            log.info("Submitting for input dataset {0}".format(sample))
            submitMap[sample] = crabClientSubmit.submit(logger,submitArgs)()
            #res = crabCommand(command, config = config, *commandArgs)
        except HTTPException as hte:
            log.info("Submission for input dataset {0} failed: {1}".format(sample, hte.headers))
        except ClientException as cle:
            log.info("Submission for input dataset {0} failed: {1}".format(sample, cle))

def status_crab(args):
    '''Check jobs'''
    crab_dirs = []
    if args.jobName:
        workArea = get_crab_workArea(args)
        crab_dirs += glob.glob('{0}/*'.format(workArea))
    elif args.crabDirectories:
        for d in args.crabDirectories:
            crab_dirs += glob.glob(d)
    else:
        log.error("Shouldn't be possible to get here")

    tblogger, logger, memhandler = initLoggers()
    tblogger.setLevel(logging.WARNING)
    logger.setLevel(logging.WARNING)
    memhandler.setLevel(logging.WARNING)

    statusMap = {}
    for d in crab_dirs:
        if os.path.exists(d):
            statusArgs = ['--dir',d]
            if args.verbose: statusArgs += ['--long']
            try:
                log.info('Retrieving status of {0}'.format(d))
                statusMap[d] = crabClientStatus.status(logger,statusArgs)()
            except HTTPException as hte:
                log.warning("Status for input directory {0} failed: {1}".format(d, hte.headers))
            except ClientException as cle:
                log.warning("Status for input directory {0} failed: {1}".format(d, cle))

    parse_crab_status(args,statusMap)

def parse_crab_status(args,statusMap):
    '''Parse the output of a crab status call'''
    allowedStatuses = ['UPLOADED','SUBMITTED','FAILED','QUEUED','SUBMITFAILED','COMPLETED','KILLED','KILLFAILED','RESUBMITFAILED','NEW','RESUBMIT','KILL','UNKNOWN']
    allowedStates = ['idle','running','transferring','finished','failed','unsubmitted','cooloff','killing','held']
    statusSummary = {}
    for status in allowedStatuses: statusSummary[status] = []
    stateSummary = {}
    for state in allowedStates: stateSummary[state] = 0
    for d,summary in statusMap.iteritems():
        status = summary['status']
        statusSummary[status] += [d]
        if 'jobs' in summary:
            for j,job in summary['jobs'].iteritems():
                stateSummary[job['State']] += 1
    log.info('Summary')
    for s in allowedStatuses:
        if statusSummary[s]:
            log.info('Status: {0}'.format(s))
            for d in statusSummary[s]:
                log.info('    {0}'.format(d))
    for s in allowedStates:
        if stateSummary[s]:
            log.info('{0:12} : {1}'.format(s,stateSummary[s]))

def resubmit_crab(args):
    '''Resubmit jobs'''
    crab_dirs = []
    if args.jobName:
        workArea = get_crab_workArea(args)
        crab_dirs += glob.glob('{0}/*'.format(workArea))
    elif args.crabDirectories:
        for d in args.crabDirectories:
            crab_dirs += glob.glob(d)
    else:
        log.error("Shouldn't be possible to get here")

    tblogger, logger, memhandler = initLoggers()
    tblogger.setLevel(logging.WARNING)
    logger.setLevel(logging.WARNING)
    memhandler.setLevel(logging.WARNING)

    resubmitMap = {}
    for d in crab_dirs:
        if os.path.exists(d):
            resubmitArgs = ['--dir',d]
            try:
                log.info('Resubmitting {0}'.format(d))
                resubmitMap[d] = crabClientResubmit.resubmit(logger,resubmitArgs)()
            except HTTPException as hte:
                log.warning("Submission for input directory {0} failed: {1}".format(d, hte.headers))
            except ClientException as cle:
                log.warning("Submission for input directory {0} failed: {1}".format(d, cle))

    for d,statMap in resubmitMap.iteritems():
        if statMap['status'] != 'SUCCESS':
            log.info('Status: {0} - {1}'.format(statMap['status'],d))


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

    # crabSubmit
    parser_crabSubmit = subparsers.add_parser('crabSubmit', help='Submit jobs via crab')
    parser_crabSubmit.add_argument('jobName', type=str, help='Job Name for submission')
    parser_crabSubmit.add_argument('cfg', type=str, help='cmsRun config file')
    parser_crabSubmit.add_argument('cmsRunArgs', nargs='*', 
        help='VarParsing arguments passed to cmsRun'
    )

    parser_crabSubmit.add_argument('--sampleList', type=str,
        help='Text file list of DAS samples to submit, one per line'
    )

    parser_crabSubmit.add_argument('--applyLumiMask',action='store_true',
        help='Apply the latest golden json run lumimask to data'
    )

    parser_crabSubmit.add_argument('--inputDBS', type=str, default='global',
        choices=['global','phys01','phys02','phys03'], 
        help='DAS instance to search for input files'
    )

    parser_crabSubmit.add_argument('--publish', action='store_true', help='Publish output to DBS')

    parser_crabSubmit.add_argument('--dryrun', action='store_true', help='Do not submit jobs')

    parser_crabSubmit.set_defaults(submit=submit_crab)

    # crabStatus
    parser_crabStatus = subparsers.add_parser('crabStatus', help='Check job status via crab')

    parser_crabStatus_directories = parser_crabStatus.add_mutually_exclusive_group(required=True)
    parser_crabStatus_directories.add_argument('--jobName', type=str, help='Job name from submission')
    parser_crabStatus_directories.add_argument('--crabDirectories', type=str, nargs="*",
        help='Space separated list of crab submission directories. Unix wild-cards allowed.',
    )

    parser_crabStatus.add_argument('--verbose', action='store_true', help='Verbose status summary')

    parser_crabStatus.set_defaults(submit=status_crab)

    # crabResubmit
    parser_crabResubmit = subparsers.add_parser('crabResubmit', help='Resubmit crab jobs')

    parser_crabResubmit_directories = parser_crabResubmit.add_mutually_exclusive_group(required=True)
    parser_crabResubmit_directories.add_argument('--jobName', type=str, help='Job name from submission')
    parser_crabResubmit_directories.add_argument('--crabDirectories', type=str, nargs="*",
        help='Space separated list of crab submission directories. Unix wild-cards allowed.',
    )

    parser_crabResubmit.set_defaults(submit=resubmit_crab)

    # condorSubmit
    parser_condorSubmit = subparsers.add_parser('condorSubmit', help='Submit jobs via condor')
    parser_condorSubmit.add_argument('jobName', type=str, help='Job Name for submission')
    parser_condorSubmit.add_argument('cfg', type=str, help='cmsRun config file')
    parser_condorSubmit.add_argument('cmsRunArgs', nargs='*', 
        help='VarParsing arguments passed to cmsRun'
    )

    parser_condorSubmit.add_argument('--sampleList', type=str, nargs=1,
        help='Text file list of DAS samples to submit, one per line'
    )

    parser_condorSubmit.add_argument('--applyLumiMask',action='store_true',
        help='Apply the latest golden json run lumimask to data'
    )

    parser_condorSubmit.add_argument('--inputDBS', type=str, default='global',
        choices=['global','phys01','phys02','phys03'], 
        help='DAS instance to search for input files'
    )

    parser_condorSubmit.add_argument('-o','--outfile',type=str,default='',
        help='Output file name to write submission commands'
    )

    parser_condorSubmit.set_defaults(submit=submit_condor)

    return parser.parse_args(argv)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    submit_string = args.submit(args)

if __name__ == "__main__":
    status = main()
    sys.exit(status)
