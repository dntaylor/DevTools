# AnalysisTree.py

import logging
import ROOT
from array import array

typeMap = {
    'I': int,
    'l': long,
    'F': float,
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
        self.branches['run']   = {'var': array('i',[0]), 'rootType': 'I', 'function': 'run'}
        self.branches['lumi']  = {'var': array('i',[0]), 'rootType': 'I', 'function': 'lumi'}
        self.branches['event'] = {'var': array('L',[0]), 'rootType': 'l', 'function': 'event'}
        self.__addBranch('run')
        self.__addBranch('lumi')
        self.__addBranch('event')

    def __addBranch(self,label):
        if label not in self.branchSet:
            self.tree.Branch(label, self.branches[label]['var'], '{0}/{1}'.format(label,self.branches[label]['rootType']))
            self.branchSet.add(label)
        else:
            logging.warning('Branch with label "{0}" already exists.'.format(label))

    def add(self, fun, label, rootType):
        if label not in self.branches:
            self.branches[label] = {'var': array(arrayMap[rootType],[0]), 'rootType': rootType, 'function': fun}
            self.__addBranch(label)
        else:
            logging.warning("{0} already in AnalysisTree.".format(label))

    def __evaluate(self,label,rtrow,cands):
        rootType = typeMap[self.branches[label]['rootType']]
        if isinstance(self.branches[label]['function'], basestring): # its just a branch in the tree
            self.branches[label]['var'][0] = rootType(getattr(rtrow,self.branches[label]['function']))
        else:
            self.branches[label]['var'][0] = rootType(self.branches[label]['function'](rtrow,cands))

    def fill(self,rtrow,cands):
        eventkey = '{0}:{1}:{2}'.format(rtrow.run, rtrow.lumi, rtrow.event)
        if eventkey in self.filled:
            logging.warning("Event {0} already filled.".format(eventkey))
        else:
            for label in self.branches:
                self.__evaluate(label,rtrow,cands)
            self.tree.Fill()
            self.filled.add(eventkey)
