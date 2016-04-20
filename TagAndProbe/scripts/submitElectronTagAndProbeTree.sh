#!/bin/bash
DATE=`date +%Y-%m-%d`
if [ "$1" == "" ]; then
    NAME="DevTools_TagAndProbe_Electron_76X_v1"
else
    NAME="$1"
fi
submit_job.py crabSubmit --sampleList DevTools/TagAndProbe/data/datasetList_MC.txt "$DATE"_"$NAME" DevTools/TagAndProbe/test/electronTagAndProbeTree_cfg.py isMC=1
submit_job.py crabSubmit --sampleList DevTools/TagAndProbe/data/datasetList_Data_Electron.txt --applyLumiMask "$DATE"_"$NAME" DevTools/TagAndProbe/test/electronTagAndProbeTree_cfg.py isMC=0
