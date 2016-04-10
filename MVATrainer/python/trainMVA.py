import os
import sys
from multiprocessing import Pool

from DevTools.MVATrainer.Hpp4lTrainer import Hpp4lTrainer



def train(mass):
    trainer = Hpp4lTrainer(
        mass=mass,
        outputFileName='mvaTraining.{0}.root'.format(mass),
        jobName='training.{0}'.format(mass),
    )
    trainer.train()
    

#train(200)

pool = Pool(16)
masses = [200,300,400,500,600,700,800,900,1000]

try:
    pool.map_async(train, masses).get(999999)
except KeyboardInterrupt:
    pool.terminate()
    print 'training cancelled'
    sys.exit(1)
