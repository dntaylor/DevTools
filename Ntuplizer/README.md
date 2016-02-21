Ntuplizer
=========

The ntuplizer produces flat root files from MiniAOD EDM files.

Events are stored if they include at least one electron, muon, or tau.

Usage
-----

Use the configuration file [MiniTree_cfg.py](test/MiniTree_cfg.py).
This configuration supports the following files:
 * MC
   * RunIIFall15MiniAODv2
 * Data
   * 16Dec2015

Options:
 * `inputFiles`: Standard cmsRun inputFiles argument for PoolSource.
 * `outputFile`: Standard cmsRun outputFile argument (uses TFileService). Default: `miniTree.root`.
 * `isMC`: Use if you are running over Monte Carlo. Default: `0` (for data).
 * `runMetFilter`: For use with data to apply the recommended MET filters. Default: `0`.

### Example

 * Data
```
cmsRun DevTools/Ntuplizer/test/MiniTree_cfg.py runMetFilter=1 inputFiles=/store/data/Run2015D/MuonEG/MINIAOD/16Dec2015-v1/60000/00D00022-37AD-E511-8380-0CC47A78A3EE.root
```

 * MC
```
cmsRun DevTools/Ntuplizer/test/MiniTree_cfg.py isMC=1 inputFiles=/store/mc/RunIIFall15MiniAODv2/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/10000/022EC2EB-90B8-E511-AED0-0026B937D37D.root
```

Grid Submission
---------------

Jobs can be submitted to the grid using the [submit_job.py](../Utilities/scripts/submit_job.py) script.

See `submit_job.py -h` for help.

You must first source the crab environment:

```
source /cvmfs/cms.cern.ch/crab3/crab.sh
```

The `--dryrun` option will tell crab to submit a test job and report the success or failure.
It will also give you estimated runtimes. When you are ready to submit, remove the `--dryrun` option.
You will also need to change the `jobName` option.

### Example

 * Data
```
submit_job.py crabSubmit --sampleList datasetList_Data.txt --applyLumiMask --dryrun testDataSubmission_v1 DevTools/Ntuplizer/test/MiniTree_cfg.py runMetFilter=1
```

 * MC
```
submit_job.py crabSubmit --sampleList datasetList_MC.txt --dryrun testMCSubmission_v1 DevTools/Ntuplizer/test/MiniTree_cfg.py isMC=1
```

