#!/usr/bin/env python
import sys
import os

import ROOT

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    histName = 'pileup'
    fileName = 'pileup/pileup.root'
    
    # 76X samples with pileup matching data
    from SimGeneral.MixingModule.mix_2015_25ns_FallMC_matchData_PoissonOOTPU_cfi import mix
    pileupDist = [float(x) for x in mix.input.nbPileupEvents.probValue]
    
    rootfile = ROOT.TFile(fileName,'recreate')
    
    # create mc pileup dist
    histmc = ROOT.TH1D(histName+'_MC',histName+'_MC',len(pileupDist),0,len(pileupDist))
    for b,val in enumerate(pileupDist):
        histmc.SetBinContent(b+1,val)
    histmc.Scale(1./histmc.Integral())
    
    histmc.Write()
    
    # read data
    for datatype in ['','_up','_down']:
        dataFileName = 'pileup/PileUpData{0}.root'.format(datatype)
        datafile = ROOT.TFile(dataFileName)
        histdata = datafile.Get(histName)
        histdata.SetTitle(histName+'_Data' + datatype)
        histdata.SetName(histName+'_Data'+datatype)
        histdata.Scale(1./histdata.Integral())
        rootfile.cd()
        histdata.Write()
    
        # now use to get scalefactors
        numbins = min([histdata.GetNbinsX(),histmc.GetNbinsX()])
        histscale = ROOT.TH1D(histName+'_scale'+datatype,histName+'_scale'+datatype,numbins,0,numbins)
        for b in range(numbins):
            d = histdata.GetBinContent(b+1)
            m = histmc.GetBinContent(b+1)
            sf = float(d)/m
            histscale.SetBinContent(b+1,sf)
        histscale.Write()
    
    rootfile.Write()
    rootfile.Close()



if __name__ == "__main__":
    status = main()
    sys.exit(status)
                    
