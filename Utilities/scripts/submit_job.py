#!/usr/bin/env python

'''
submit_job.py

Script to submit jobs to crab or condor.
'''

import argparse
import logging
import os
import math
import sys
import glob
import subprocess
from socket import gethostname

log = logging.getLogger("submit_job")
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

try:
    from CRABClient.ClientExceptions import ClientException
    from CRABClient.ClientUtilities import initLoggers
    from httplib import HTTPException
    import CRABClient.Commands.submit as crabClientSubmit
    import CRABClient.Commands.status as crabClientStatus
    import CRABClient.Commands.resubmit as crabClientResubmit
    crabLoaded = True
except:
    crabLoaded = False



def get_crab_workArea(args):
    '''Get the job working area'''
    uname = os.environ['USER']
    scratchDir = 'data' if 'uwlogin' in gethostname() else 'nfs_scratch'
    return '/{0}/{1}/crab_projects/{2}'.format(scratchDir,uname,args.jobName)

def strip_hdfs(directory):
    return '/'.join([x for x in directory.split('/') if x not in ['hdfs']])

def hdfs_ls_directory(storeDir):
    '''Utility for ls'ing /hdfs at UW'''
    storeDir = strip_hdfs(storeDir)
    command = 'gfal-ls srm://cmssrm2.hep.wisc.edu:8443/srm/v2/server?SFN=/hdfs/{0}'.format(storeDir)
    out = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    if 'gfal-ls' in out:
        log.error(out)
        return []
    return out.split()

def get_hdfs_root_files(topDir,lastDir):
    '''Utility for getting all root files in a directory (and subdirectories)'''
    lsDir = strip_hdfs('{0}/{1}'.format(topDir,lastDir))
    nextLevel = hdfs_ls_directory(lsDir)
    out = []
    for nl in nextLevel:
        if nl=='failed': # dont include
            continue
        elif nl[-4:]=='root': # its a root file
            out += ['{0}/{1}'.format(lsDir,nl)]
        else: # keep going down
            out += get_hdfs_root_files(lsDir,nl)
    return out

def get_config(args):
    '''Get a crab config file based on the arguments of crabSubmit'''
    uname = os.environ['USER']
    from CRABClient.UserUtilities import config

    config = config()

    config.General.workArea         = get_crab_workArea(args)
    config.General.transferOutputs  = True

    config.JobType.pluginName       = 'Analysis'
    #if args.scriptExe:
    #    config.JobType.psetName     = '{0}/src/DevTools/Utilities/test/PSet.py'.format(os.environ['CMSSW_BASE'])
    #    config.JobType.scriptExe    = args.cfg
    #else:
    config.JobType.psetName         = args.cfg
    config.JobType.pyCfgParams      = args.cmsRunArgs
    #if args.scriptExe: # add in the outputFile
    #    config.JobType.pyCfgParams += ['--outputFile=crab_out.root']
    #    config.JobType.outputFiles  = ['crab_out.root']
    config.JobType.sendPythonFolder = True

    config.Data.inputDBS            = args.inputDBS
    config.Data.splitting           = 'FileBased'
    config.Data.unitsPerJob         = args.filesPerJob
    #config.Data.splitting           = 'LumiBased'
    #config.Data.unitsPerJob         = 10
    #config.Data.splitting           = 'EventAwareLumiBased'
    #config.Data.unitsPerJob         = 100000
    config.Data.outLFNDirBase       = '/store/user/{0}/{1}/'.format(uname,args.jobName)
    config.Data.publication         = args.publish
    config.Data.outputDatasetTag    = args.jobName
    if args.applyLumiMask=='Collisions15':
        config.Data.lumiMask        = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/'\
                                      'Collisions15/13TeV/'\
                                      'Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt'
    if args.applyLumiMask=='Collisions16':
        config.Data.lumiMask        = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/'\
                                      'Collisions16/13TeV/'\
                                      'Cert_271036-273450_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'
        #config.Data.splitting       = 'LumiBased'
        #config.Data.unitsPerJob     = args.lumisPerJob

    config.Site.storageSite         = 'T2_US_Wisconsin'

    return config

def submit_das_crab(args):
    '''Submit samples using DAS'''
    tblogger, logger, memhandler = initLoggers()
    tblogger.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    memhandler.setLevel(logging.INFO)

    # crab config
    config = get_config(args)

    # get samples
    sampleList = []
    if args.samples:
        sampleList += args.samples
    elif os.path.isfile(args.sampleList):
        with open(args.sampleList,'r') as f:
            sampleList = [line.strip() for line in f]
    else:
        log.error('Sample input list {0} does not exist.'.format(args.sampleList))

    submitMap = {}
    # iterate over samples
    for sample in sampleList:
        _, primaryDataset, datasetTag, dataFormat = sample.split('/')
        config.General.requestName = '{0}'.format(primaryDataset)
        maxDatasetTagSize = 97-len(primaryDataset)
        config.General.requestName += '_' + datasetTag[-maxDatasetTagSize:]
        # make it only 100 characters
        config.General.requestName = config.General.requestName[:99] # Warning: may not be unique now
        config.Data.inputDataset   = sample
        # submit the job
        submitArgs = ['--config',config]
        if args.dryrun: submitArgs += ['--dryrun']
        try:
            log.info("Submitting for input dataset {0}".format(sample))
            submitMap[sample] = crabClientSubmit.submit(logger,submitArgs)()
        except HTTPException as hte:
            log.info("Submission for input dataset {0} failed: {1}".format(sample, hte.headers))
        except ClientException as cle:
            log.info("Submission for input dataset {0} failed: {1}".format(sample, cle))

def submit_untracked_crab(args):
    '''Submit jobs from an inputDirectory'''
    tblogger, logger, memhandler = initLoggers()
    tblogger.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    memhandler.setLevel(logging.INFO)

    # crab config
    config = get_config(args)
    config.Site.whitelist = ['T2_US_Wisconsin'] # whitelist wisconsin so it only runs there


    # get samples
    sampleList = hdfs_ls_directory(args.inputDirectory)

    submitMap = {}
    # iterate over samples
    for sample in sampleList:
        primaryDataset = sample
        config.General.requestName = '{0}'.format(primaryDataset)
        # make it only 100 characters
        config.General.requestName = config.General.requestName[:99] # Warning: may not be unique now
        config.Data.outputPrimaryDataset = primaryDataset
        # get file list
        config.Data.userInputFiles = get_hdfs_root_files(args.inputDirectory,sample)
        # submit the job
        submitArgs = ['--config',config]
        if args.dryrun: submitArgs += ['--dryrun']
        try:
            log.info("Submitting for input dataset {0}".format(sample))
            submitMap[sample] = crabClientSubmit.submit(logger,submitArgs)()
        except HTTPException as hte:
            log.info("Submission for input dataset {0} failed: {1}".format(sample, hte.headers))
        except ClientException as cle:
            log.info("Submission for input dataset {0} failed: {1}".format(sample, cle))


def submit_crab(args):
    '''Create submission script for crab'''
    if not crabLoaded:
        logging.error('You must source a crab environment to submit to crab.\nsource /cvmfs/cms.cern.ch/crab3/crab.sh')
        return
    if args.sampleList or args.samples:
        submit_das_crab(args)
    elif args.inputDirectory:
        submit_untracked_crab(args)
    else:
        log.warning('Unrecognized submit configuration.')


def status_crab(args):
    '''Check jobs'''
    if not crabLoaded:
        logging.error('You must source a crab environment to submit to crab.\nsource /cvmfs/cms.cern.ch/crab3/crab.sh')
        return
    crab_dirs = []
    if args.jobName:
        workArea = get_crab_workArea(args)
        crab_dirs += sorted(glob.glob('{0}/*'.format(workArea)))
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
            #if args.verbose: statusArgs += ['--long']
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
    allowedStatuses = ['COMPLETED','UPLOADED','SUBMITTED','FAILED','QUEUED','SUBMITFAILED','KILLED','KILLFAILED','RESUBMITFAILED','NEW','RESUBMIT','KILL','UNKNOWN']
    allowedStates = ['idle','running','transferring','finished','failed','unsubmitted','cooloff','killing','held']
    statusSummary = {}
    for status in allowedStatuses: statusSummary[status] = []
    singleStateSummary = {}
    stateSummary = {}
    for state in allowedStates: stateSummary[state] = 0
    for d,summary in statusMap.iteritems():
        status = summary['status']
        statusSummary[status] += [d]
        if 'jobs' in summary:
            singleStateSummary[d] = {}
            for state in allowedStates: singleStateSummary[d][state] = 0
            for j,job in summary['jobs'].iteritems():
                singleStateSummary[d][job['State']] += 1
                stateSummary[job['State']] += 1
    log.info('Summary')
    for s in allowedStatuses:
        if statusSummary[s]:
            log.info('Status: {0}'.format(s))
            for d in sorted(statusSummary[s]):
                log.info('    {0}'.format(d))
                if args.verbose:
                    for s in allowedStates:
                        if singleStateSummary[d][s]:
                            log.info('        {0:12} : {1}'.format(s,singleStateSummary[d][s]))
    for s in allowedStates:
        if stateSummary[s]:
            log.info('{0:12} : {1}'.format(s,stateSummary[s]))

def resubmit_crab(args):
    '''Resubmit jobs'''
    if not crabLoaded:
        logging.error('You must source a crab environment to submit to crab.\nsource /cvmfs/cms.cern.ch/crab3/crab.sh')
        return
    crab_dirs = []
    if args.jobName:
        workArea = get_crab_workArea(args)
        crab_dirs += sorted(glob.glob('{0}/*'.format(workArea)))
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
            statusArgs = ['--dir',d]
            resubmitArgs = ['--dir',d]
            try:
                summary = crabClientStatus.status(logger,statusArgs)()
                resubmit = False
                total = 0
                failed = 0
                if 'jobs' in summary:
                    for j,job in summary['jobs'].iteritems():
                        total += 1
                        if job['State'] in ['failed']:
                            failed += 1
                            resubmit = True
                if resubmit:
                    log.info('Resubmitting {0}'.format(d))
                    log.info('{0} of {1} jobs failed'.format(failed,total))
                    resubmitMap[d] = crabClientResubmit.resubmit(logger,resubmitArgs)()
            except HTTPException as hte:
                log.warning("Submission for input directory {0} failed: {1}".format(d, hte.headers))
            except ClientException as cle:
                log.warning("Submission for input directory {0} failed: {1}".format(d, cle))

    for d,statMap in resubmitMap.iteritems():
        if statMap['status'] != 'SUCCESS':
            log.info('Status: {0} - {1}'.format(statMap['status'],d))

def get_condor_workArea(args):
    '''Get the job working area'''
    uname = os.environ['USER']
    scratchDir = 'data' if 'uwlogin' in gethostname() else 'nfs_scratch'
    return '/{0}/{1}/condor_projects/{2}'.format(scratchDir,uname,args.jobName)


def hdfs_directory_size(directory):
    '''Get the size of a hdfs directory (in bytes).'''
    directory = strip_hdfs(directory)
    command = 'gsido hdfs dfs -du -s {0}'.format(directory)
    out = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    return float(out.split()[0])

def submit_untracked_condor(args):
    '''Submit to condor using an input directory'''
    uname = os.environ['USER']
    # get samples
    for inputDirectories in args.inputDirectory:
        for inputDirectory in glob.glob(inputDirectories):
            sampleList = hdfs_ls_directory(inputDirectory)
            scratchDir = 'data' if 'uwlogin' in gethostname() else 'nfs_scratch'

            workArea = get_condor_workArea(args)
            os.system('mkdir -p {0}'.format(workArea))

            submitMap = {}
            # iterate over samples
            for sample in sampleList:
                # farmout config
                command = 'farmoutAnalysisJobs --infer-cmssw-path'
                if hasattr(args,'scriptExe') and args.scriptExe:
                    command += ' --fwklite'
                # submit dir
                submitDir = '{0}/{1}'.format(workArea, sample)
                command += ' --submit-dir={0}'.format(submitDir)
                # input files
                inputFiles = get_hdfs_root_files(inputDirectory,sample)
                totalFiles = len(inputFiles)
                if totalFiles==0:
                    logging.warning('{0} {1} has no files.'.format(inputDirectory,sample))
                    continue
                fileList = '{0}_inputs.txt'.format(submitDir)
                with open(fileList,'w') as f:
                    f.write('\n'.join(inputFiles))
                filesPerJob = args.filesPerJob
                if args.gigabytesPerJob:
                    totalSize = hdfs_directory_size(os.path.join(inputDirectory,sample))
                    averageSize = totalSize/totalFiles
                    GB = 1024.*1024.*1024.
                    filesPerJob = int(math.ceil(args.gigabytesPerJob*GB/averageSize))
                command += ' --input-file-list={0} --assume-input-files-exist --input-files-per-job={1}'.format(fileList,filesPerJob)
                # output directory
                outputDir = 'srm://cmssrm2.hep.wisc.edu:8443/srm/v2/server?SFN=/hdfs/store/user/{0}/{1}/{2}'.format(uname,args.jobName,sample)
                command += ' --output-dir={0}'.format(outputDir)
                if args.useHDFS: command += ' --use-hdfs'
                if hasattr(args,'cfg'):
                    command += ' {0} {1} {2}'.format(args.jobName, args.cfg, ' '.join(args.cmsRunArgs))
                else: # its a merge
                    command += ' --merge {0}'.format(args.jobName)
                if args.dryrun:
                    logging.info(command)
                else:
                    os.system(command)
        

def submit_condor(args):
    '''Create submission script for condor'''
    if args.inputDirectory:
        submit_untracked_condor(args)
    else:
        log.warning('Unrecognized submit configuration.')

def status_condor(args):
    '''Check jobs on condor'''
    condor_dirs = []
    if args.jobName:
        workArea = get_condor_workArea(args)
        condor_dirs += sorted(glob.glob('{0}/*'.format(workArea)))
    elif args.condorDirectories:
        for d in args.condorDirectories:
            condor_dirs += glob.glob(d)
    else:
        log.error("Shouldn't be possible to get here")

    allowedStatuses = ['SUBMITTED','RUNNING','ERROR','EVICTED','ABORTED','SUSPENDED','HELD','FINISHED','UNKNOWN']

    logstatuses = { # TODO: lookup possible states
        0 : 'SUBMITTED',
        1 : 'RUNNING',
        2 : 'ERROR',
        4 : 'EVICTED',
        5 : 'FINISHED',
        9 : 'ABORTED',
        10: 'SUSPENDED',
        11: 'RUNNING', #'UNSUSPENDED',
        12: 'HELD',
        13: 'RUNNING', #'RELEASED',
    }
    results = {}
    for d in sorted(condor_dirs):
        if os.path.isdir(d):
            results[d] = {}
            # get list of jobs
            jobDirs = [j for j in glob.glob('{0}/*'.format(d)) if os.path.isdir(j)]
            for j in jobDirs:
                results[d][j] = {}
                # completed jobs have a report.log in the submission directory
                if os.path.exists('{0}/report.log'.format(j)):
                    # parse report.log TODO lookup possible exit codes
                    results[d][j]['status'] = 'FINISHED'
                else:
                    # load log file
                    logfile = '{0}/{1}.log'.format(j,os.path.basename(j))
                    if os.path.exists(logfile):
                        laststatus = ''
                        with open(logfile,'r') as f:
                            for line in f.readlines():
                                if 'TriggerEventTypeNumber' in line:
                                    code = int(line.split()[-1])
                                    if code in logstatuses: 
                                        laststatus = logstatuses[code]
                        results[d][j]['status'] = laststatus
                    else:
                        results[d][j]['status'] = 'UNKNOWN'

    # print out the summary
    total = {}
    for s in allowedStatuses: total[s] = 0
    for d in sorted(results):
        if args.verbose: log.info(d)
        for s in allowedStatuses:
            jobs = [key for key,val in results[d].iteritems() if val['status']==s]
            total[s] += len(jobs)
            if len(jobs) and args.verbose: log.info('    {0:20}: {1}'.format(s,len(jobs)))
    for s in allowedStatuses:
        if total[s]: log.info('{0:20}: {1}'.format(s,total[s]))

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Submit jobs to grid')

    # submission type
    subparsers = parser.add_subparsers(help='Submission mode')

    # crabSubmit
    parser_crabSubmit = subparsers.add_parser('crabSubmit', help='Submit jobs via crab')
    parser_crabSubmit.add_argument('jobName', type=str, help='Job Name for submission')
    parser_crabSubmit.add_argument('cfg', type=str, help='cmsRun config file or user script')
    parser_crabSubmit.add_argument('cmsRunArgs', nargs='*', 
        help='Arguments passed to cmsRun/script'
    )

    parser_crabSubmit_inputs = parser_crabSubmit.add_mutually_exclusive_group(required=True)
    parser_crabSubmit_inputs.add_argument('--samples', type=str, nargs='*',
        help='Space delimited list of DAS samples to submit'
    )
    parser_crabSubmit_inputs.add_argument('--sampleList', type=str,
        help='Text file list of DAS samples to submit, one per line'
    )
    parser_crabSubmit_inputs.add_argument('--inputDirectory', type=str,
        help='Top level directory to submit. Each subdirectory will create one crab job.'
    )

    parser_crabSubmit.add_argument('--applyLumiMask',type=str, default=None,
        choices=['Collisions15','Collisions16'],
        help='Apply the latest golden json run lumimask to data'
    )

    parser_crabSubmit.add_argument('--inputDBS', type=str, default='global',
        choices=['global','phys01','phys02','phys03'], 
        help='DAS instance to search for input files'
    )

    parser_crabSubmit.add_argument('--filesPerJob', type=int, default=1,
        help='Number of files per job'
    )
    parser_crabSubmit.add_argument('--lumisPerJob', type=int, default=30,
        help='Number of lumis per job'
    )

    parser_crabSubmit.add_argument('--publish', action='store_true', help='Publish output to DBS')

    parser_crabSubmit.add_argument('--dryrun', action='store_true', help='Do not submit jobs')

    #parser_crabSubmit.add_argument('--scriptExe', action='store_true', help='This is a script, not a cmsRun config')

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

    parser_condorSubmit_inputs = parser_condorSubmit.add_mutually_exclusive_group(required=True)
    parser_condorSubmit_inputs.add_argument('--samples', type=str, nargs='*',
        help='Space delimited list of DAS samples to submit'
    )
    parser_condorSubmit_inputs.add_argument('--sampleList', type=str,
        help='Text file list of DAS samples to submit, one per line'
    )
    parser_condorSubmit_inputs.add_argument('--inputDirectory', type=str, nargs='*',
        help='Top level directory to submit (unix wildcards allowed). Each subdirectory will create one condor job.'
    )

    parser_condorSubmit.add_argument('--applyLumiMask',type=str, default=None,
        choices=['Collisions15','Collisions16'],
        help='Apply the latest golden json run lumimask to data'
    )

    parser_condorSubmit.add_argument('--inputDBS', type=str, default='global',
        choices=['global','phys01','phys02','phys03'], 
        help='DAS instance to search for input files'
    )

    parser_condorSubmit_jobs = parser_condorSubmit.add_mutually_exclusive_group(required=True)
    parser_condorSubmit_jobs.add_argument('--filesPerJob', type=int, default=1,
        help='Number of files per job'
    )

    parser_condorSubmit_jobs.add_argument('--gigabytesPerJob', type=float, default=0,
        help='Average jobs to process a given number of gigabytes'
    )

    parser_condorSubmit.add_argument('--dryrun', action='store_true', help='Do not submit jobs')

    parser_condorSubmit.add_argument('--useHDFS', action='store_true', help='Use HDFS to read files')

    parser_condorSubmit.add_argument('--scriptExe', action='store_true', help='This is a script, not a cmsRun config')

    parser_condorSubmit.set_defaults(submit=submit_condor)

    # condorStatus
    parser_condorStatus = subparsers.add_parser('condorStatus', help='Check job status via condor')

    parser_condorStatus_directories = parser_condorStatus.add_mutually_exclusive_group(required=True)
    parser_condorStatus_directories.add_argument('--jobName', type=str, help='Job name from submission')
    parser_condorStatus_directories.add_argument('--condorDirectories', type=str, nargs="*",
        help='Space separated list of condor submission directories. Unix wild-cards allowed.',
    )

    parser_condorStatus.add_argument('--verbose', action='store_true', help='Verbose status summary')

    parser_condorStatus.set_defaults(submit=status_condor)

    # condorMerge
    parser_condorMerge = subparsers.add_parser('condorMerge', help='Submit merge job via condor')
    parser_condorMerge.add_argument('jobName', type=str, help='Job Name for submission')

    parser_condorMerge_inputs = parser_condorMerge.add_mutually_exclusive_group(required=True)

    parser_condorMerge_inputs.add_argument('--inputDirectory', type=str, nargs='*',
        help='Top level directory to submit (unix wildcards allowed). Each subdirectory will create one condor job.'
    )

    parser_condorMerge_jobs = parser_condorMerge.add_mutually_exclusive_group(required=True)
    parser_condorMerge_jobs.add_argument('--filesPerJob', type=int, default=1,
        help='Number of files per job'
    )

    parser_condorMerge_jobs.add_argument('--gigabytesPerJob', type=float, default=0,
        help='Average jobs to process a given number of gigabytes'
    )

    parser_condorMerge.add_argument('--dryrun', action='store_true', help='Do not submit jobs')

    parser_condorMerge.add_argument('--useHDFS', action='store_true', help='Use HDFS to read files')

    parser_condorMerge.set_defaults(submit=submit_condor)

    return parser.parse_args(argv)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    submit_string = args.submit(args)

if __name__ == "__main__":
    status = main()
    sys.exit(status)
