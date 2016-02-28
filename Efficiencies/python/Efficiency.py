import logging
import os
import sys
import time

import ROOT
from array import array

class Efficiency(object):
    '''Calculates the efficiency on a tree'''

    def __init__(self,**kwargs):
        inputFileNames = kwargs.pop('inputFileNames',[])
        inputTreeDirectory = kwargs.pop('inputTreeDirectory','miniTree')
        inputTreeName = kwargs.pop('inputTreeName','MiniTree')
        inputLumiName = kwargs.pop('inputTreeName','LumiTree')
        outputFileName = kwargs.pop('outputFileName','efficiency.root')
        # input files
        self.fileNames = []
        if isinstance(inputFileNames, basestring): # inputFiles is a file name
            if os.path.isfile(inputFileNames):     # single file
                if inputFileNames[-4:] == 'root':  # file is a root file
                    self.fileNames += [inputFileNames]
                else:                          # file is list of files
                    with open(inputFileNames,'r') as f:
                        for line in f:
                            self.fileNames += [line.strip()]
        else:
            self.fileNames = inputFileNames # already a python list or a cms.untracked.vstring()
        if not isinstance(outputFileName, basestring): # its a cms.string(), get value
            outputFileName = outputFileName.value()
        # input tchain
        self.tchain = ROOT.TChain('{0}/{1}'.format(inputTreeDirectory,inputTreeName))
        self.tchainLumi = ROOT.TChain('{0}/{1}'.format(inputTreeDirectory,inputLumiName))
        for fName in self.fileNames:
            if fName.startswith('/store'): fName = 'root://cmsxrootd.hep.wisc.edu//{0}'.format(fName)
            self.tchain.Add(fName)
            self.tchainLumi.Add(fName)
        # get the lumi info
        self.numLumis = self.tchainLumi.GetEntries()
        self.numEvents = 0
        self.summedWeights = 0
        for entry in xrange(self.numLumis):
            self.tchainLumi.GetEntry(entry)
            self.numEvents += self.tchainLumi.nevents
            self.summedWeights += self.tchainLumi.summedWeights
        logging.info("Will process {0} lumi sections with {1} events ({2}).".format(self.numLumis,self.numEvents,self.summedWeights))
        self.flush()
        # tfile
        os.system('mkdir -p {0}'.format(os.path.dirname(outputFileName)))
        self.outfile = ROOT.TFile(outputFileName,"recreate")
        # histograms
        self.histograms = {}
        self.histNames = []

    def __exit__(self, type, value, traceback):
        self.finish()

    def __del__(self):
        self.finish()

    def finish(self):
        self.outfile.Close()

    def __ratio(self):
        logging.info('Saving histograms')
        for name in self.histNames:
            if name in self.histograms: continue # its a var, not a ratio
            # divide the ratio
            ratio = self.histograms['{0}_ratio'.format(name)]
            denom = self.histograms['{0}_denominator'.format(name)]
            ratio.Divide(denom)
        self.outfile.Write()

    def flush(self):
        sys.stdout.flush()
        sys.stderr.flush()

    #############################
    ### primary analysis loop ###
    #############################
    def analyze(self):
        '''
        The primary analyzer loop.
        '''
        logging.info('Beginning Analysis')
        start = time.time()
        treeEvents = self.tchain.GetEntries()
        rtrow = self.tchain
        try:
            for r in xrange(treeEvents):
                if r==2: start = time.time() # just ignore first event for timing
                rtrow.GetEntry(r)
                if r % 1000 == 1:
                    cur = time.time()
                    elapsed = cur-start
                    remaining = float(elapsed)/r * float(treeEvents) - float(elapsed)
                    mins, secs = divmod(int(remaining),60)
                    hours, mins = divmod(mins,60)
                    logging.info('Processing event {0}/{1} - {2}:{3:02d}:{4:02d} remaining'.format(r,treeEvents,hours,mins,secs))
                    self.flush()

                self.cache = {} # cache variables so you dont read from tree as much

                self.fill(rtrow)

            self.__ratio()
        except KeyboardInterrupt:
            self.__ratio()


    def fill(self,rtrow):
        '''Dummy fill method, override and fill your histograms'''
        pass

    def getObjectVariable(self, rtrow, cand, var):
        '''
        Simple utility to get variables
        '''
        if len(cand)!=2:
            return 0
        coll, pos = cand
        key = '{0}_{1}_{2}'.format(coll,var,pos)
        if key in self.cache: return self.cache[key]

        # first, if invalid, return 0
        if pos<0:
            val = 0

        # the variable is in the input tree
        elif hasattr(rtrow,'{0}_{1}'.format(coll,var)):
            val = getattr(rtrow,'{0}_{1}'.format(coll,var))[pos]

        # get a TLorentzVector
        elif var=='p4':
            pt     = self.getObjectVariable(rtrow,cand,'pt')
            eta    = self.getObjectVariable(rtrow,cand,'eta')
            phi    = self.getObjectVariable(rtrow,cand,'phi')
            energy = self.getObjectVariable(rtrow,cand,'energy')
            val = ROOT.TLorentzVector()
            val.SetPtEtaPhiE(pt,eta,phi,energy)

        # didnt catch it
        else:
            val = 0

        self.cache[key] = val
        return val


    ################################
    ### Add efficiency histogram ###
    ################################
    def addEfficiency(self,name,binning):
        '''Add 3 histograms to file, numerator, denominator, ratio'''
        # check binning
        self.histNames += [name]
        if len(binning)==3: # its a standard thing
            self.histograms['{0}_numerator'.format(name)] = ROOT.TH1F('h_{0}_numerator'.format(name),'',*binning)
            self.histograms['{0}_denominator'.format(name)] = ROOT.TH1F('h_{0}_denominator'.format(name),'',*binning)
            self.histograms['{0}_ratio'.format(name)] = ROOT.TH1F('h_{0}_ratio'.format(name),'',*binning)
        else: # we need to do variable binning
            self.histograms['{0}_numerator'.format(name)] = ROOT.TH1F('h_{0}_numerator'.format(name),'',len(binning)-1,array('d',binning))
            self.histograms['{0}_denominator'.format(name)] = ROOT.TH1F('h_{0}_denominator'.format(name),'',len(binning)-1,array('d',binning))
            self.histograms['{0}_ratio'.format(name)] = ROOT.TH1F('h_{0}_ratio'.format(name),'',len(binning)-1,array('d',binning))

    def addVariable(self,name,binning):
        '''Add histograms to file'''
        # check binning
        self.histNames += [name]
        if len(binning)==3: # its a standard thing
            self.histograms[name] = ROOT.TH1F('h_{0}'.format(name),'',*binning)
        else: # we need to do variable binning
            self.histograms[name] = ROOT.TH1F('h_{0}'.format(name),'',len(binning)-1,array('d',binning))

    def fillEfficiency(self,name,varValue,passing,weight=1.):
        '''Fill the efficiency'''
        self.histograms['{0}_denominator'.format(name)].Fill(varValue,weight)
        if passing:
            self.histograms['{0}_numerator'.format(name)].Fill(varValue,weight)
            self.histograms['{0}_ratio'.format(name)].Fill(varValue,weight) # for dividing later

    def fillVariable(self,name,varValue,weight=1.):
        '''Fill the variable'''
        self.histograms[name].Fill(varValue,weight)
