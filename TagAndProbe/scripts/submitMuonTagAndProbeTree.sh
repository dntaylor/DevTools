#!/bin/bash
DATE=`date +%Y-%m-%d`
if [ "$1" == "" ]; then
    NAME="DevTools_TagAndProbe_Muon_76X_v1"
else
    NAME="$1"
fi
submit_job.py crabSubmit --sampleList $CMSSW_BASE/src/DevTools/TagAndProbe/data/datasetList_TagAndProbe_MC.txt --filesPerJob 30 "$DATE"_"$NAME" DevTools/TagAndProbe/test/muonTagAndProbeTree_cfg.py isMC=1
submit_job.py crabSubmit --sampleList $CMSSW_BASE/src/DevTools/TagAndProbe/data/datasetList_TagAndProbe_Data_Muon.txt --filesPerJob 30 --applyLumiMask "$DATE"_"$NAME" DevTools/TagAndProbe/test/muonTagAndProbeTree_cfg.py isMC=0
