#!/bin/bash
DATE=`date +%Y-%m-%d`
if [ "$1" == "" ]; then
    NAME="DevTools_76X_v1"
else
    NAME="$1"
fi
submit_job.py crabSubmit --sampleList DevTools/Ntuplizer/data/datasetList_MC.txt "$DATE"_"$NAME" DevTools/Ntuplizer/test/MiniTree_cfg.py isMC=1
submit_job.py crabSubmit --sampleList DevTools/Ntuplizer/data/datasetList_Data.txt --applyLumiMask "$DATE"_"$NAME" DevTools/Ntuplizer/test/MiniTree_cfg.py runMetFilter=1
submit_job.py crabSubmit --sampleList DevTools/Ntuplizer/data/datasetList_phys03.txt --inputDBS phys03 "$DATE"_"$NAME" DevTools/Ntuplizer/test/MiniTree_cfg.py isMC=1
