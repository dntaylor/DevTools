# MultiProgress.py
import signal
import sys
import time
import logging
import logging.handlers
from multiprocessing import Pool, current_process, Process, Queue
from blessings import Terminal
from progressbar import ProgressBar, Bar, ETA, Percentage, SimpleProgress

term = Terminal()

class Writer(object):
    '''
    A writer object that prints strings to a line of a terminal.
    '''
    def __init__(self,location):
        self.location = location

    def write(self,string):
        with term.location(*self.location):
            print(string)

def func_wrapper(name, func, func_args, func_kwargs):
    proc_num = current_process()._identity
    location = (0,proc_num[0]-1)
    writer = Writer(location)
    pbar = ProgressBar(widgets=['{0}: '.format(name),' ',SimpleProgress(),' ',Percentage(),' ',Bar(),' ',ETA()],fd=writer,term_width=term.width)
    return func(*func_args,progressbar=pbar,**func_kwargs)


class MultiProgress(object):
    '''
    A class to print multiple progress bars from a pool.
    '''
    def __init__(self,numCores,**kwargs):
        self.numCores = numCores
        term.move(0,term.height-self.numCores-1)
        self.orig_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.pool = Pool(self.numCores)
        signal.signal(signal.SIGINT, self.orig_sigint_handler)
        self.results = []

    def addJob(self,name,func,args=[],kwargs={}):
        '''
        Add a job to the parallel running.
            name  : name of job
            func  : function to map in pool
            args  : arguments for function
            kwargs: kwargs for function
        '''
        self.results += [self.pool.apply_async(func_wrapper,args=(name,func,args,kwargs))]

    def retrieve(self):
        '''
        Execute the jobs
        '''
        print term.enter_fullscreen
        try:
            theResult = [r.get(9999999999) for r in self.results]
        except:
            self.pool.terminate()
            theResult = []
        else:
            self.pool.close()
        self.pool.join()
        print term.exit_fullscreen
        return theResult
