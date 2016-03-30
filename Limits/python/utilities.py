import logging
import os
import sys

import ROOT

def readCount(fileNames,directories,doError=False):
    val = 0.
    err2 = 0.
    for fileName in fileNames:
        if not os.path.isfile(fileName):
            logging.warning('{0} file does not exist.'.format(fileName))
            continue
        tfile = ROOT.TFile.Open(fileName)
        for directory in directories:
            histName = '{0}/count'.format(directory)
            hist = tfile.Get(histName)
            if hist:
                val += hist.GetBinContent(1)
                err2 += hist.GetBinError(1)**2
        tfile.Close()
    return val, err2**0.5 if doError else val


