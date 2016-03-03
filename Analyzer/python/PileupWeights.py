import sys
import os
import json

from math import floor

import ROOT


class PileupWeights(object):

    def __init__(self):
        path = '{0}/src/DevTools/Analyzer/data/pileup_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12.root'.format(os.environ['CMSSW_BASE'])
        self.scale = {}
        self.scale_up = {}
        self.scale_down = {}
        rootfile = ROOT.TFile(path)
        hist_scale = rootfile.Get('pileup_scale')
        for b in range(hist_scale.GetNbinsX()):
            self.scale[b] = hist_scale.GetBinContent(b+1)
        hist_scale = rootfile.Get('pileup_scale_up')
        for b in range(hist_scale.GetNbinsX()):
            self.scale_up[b] = hist_scale.GetBinContent(b+1)
        hist_scale = rootfile.Get('pileup_scale_down')
        for b in range(hist_scale.GetNbinsX()):
            self.scale_down[b] = hist_scale.GetBinContent(b+1)
        rootfile.Close()


    def weight(self, rtrow):
        if rtrow.nTrueVertices < 0:
            return [1,1,1]
        else:
            val = self.scale[int(floor(rtrow.nTrueVertices))]
            up = self.scale_up[int(floor(rtrow.nTrueVertices))]
            down = self.scale_down[int(floor(rtrow.nTrueVertices))]
            return [val,up,down]
