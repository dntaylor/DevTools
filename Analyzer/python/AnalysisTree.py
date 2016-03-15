# AnalysisTree.py

import logging
import ROOT
from array import array


typeMap = {
    'I': int,
    'l': long,
    'F': float,
    'C': str,
}
arrayMap = {
    'I': 'i',
    'l': 'L',
    'F': 'f',
}

class AnalysisTree(object):
    '''
    Wrapper for the analysis tree
    '''
    def __init__(self,name):
        self.tree = ROOT.TTree(name,name)
        self.filled = set()
        self.branches = {}
        self.branchSet = set()
        self.branches['run']   = {'var': array('i',[0]), 'rootType': 'I', 'function': 'run', 'branchName': 'run'}
        self.branches['lumi']  = {'var': array('i',[0]), 'rootType': 'I', 'function': 'lumi', 'branchName': 'lumi'}
        self.branches['event'] = {'var': array('L',[0]), 'rootType': 'l', 'function': 'event', 'branchName': 'event'}
        self.__addBranch('run')
        self.__addBranch('lumi')
        self.__addBranch('event')

    def __addBranch(self,label):
        if label not in self.branchSet:
            self.tree.Branch(label, self.branches[label]['var'], '{0}/{1}'.format(self.branches[label]['branchName'],self.branches[label]['rootType']))
            self.branchSet.add(label)
        else:
            logging.error('Branch with label "{0}" already exists.'.format(label))

    def add(self, fun, label, rootType):
        if label not in self.branches:
            if rootType[0]=='C': # special handling of string
                self.branches[label] = {'var': bytearray(rootType[1]), 'rootType': rootType[0], 'function': fun, 'branchName': '{0}[{1}]'.format(label,rootType[1]), 'size': rootType[1]}
            else:
                self.branches[label] = {'var': array(arrayMap[rootType],[0]), 'rootType': rootType, 'function': fun, 'branchName': label}
            self.__addBranch(label)
        else:
            logging.error("{0} already in AnalysisTree.".format(label))
            raise ValueError("{0} already in AnalysisTree.".format(label))

    def __evaluate(self,label,rtrow,cands):
        pyType = typeMap[self.branches[label]['rootType']]
        if isinstance(self.branches[label]['function'], basestring): # its just a branch in the tree
            self.branches[label]['var'][0] = pyType(getattr(rtrow,self.branches[label]['function']))
        else:
            if self.branches[label]['rootType']=='C': # special handling of string
                strSize = self.branches[label]['size']
                funcVal = pyType(self.branches[label]['function'](rtrow,cands))
                if len(funcVal)==strSize-1:
                    self.branches[label]['var'][:strSize] = funcVal
                else:
                    logging.error('Size mismatch function with label {0}.'.format(label))
            else:
                self.branches[label]['var'][0] = pyType(self.branches[label]['function'](rtrow,cands))

    def fill(self,rtrow,cands,**kwargs):
        allowDuplicates = kwargs.pop('allowDuplicates',False)
        eventkey = '{0}:{1}:{2}'.format(rtrow.run, rtrow.lumi, rtrow.event)
        if eventkey in self.filled and not allowDuplicates:
            logging.warning("Event {0} already filled.".format(eventkey))
        else:
            for label in self.branches:
                self.__evaluate(label,rtrow,cands)
            self.tree.Fill()
            self.filled.add(eventkey)
