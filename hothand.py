#!/usr/bin/env python
# Author: Karthikeyan Madathil <kmadathil@gmail.com>

# Copyright 2018 Karthikeyan Madathil
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function
import numpy as np
import pandas as pd
import datetime
import argparse
import logging

logger = logging.getLogger(__name__)


def hothand(n=100,p=.5,k=3,it=1000,debug=True):
    logger.info("Players: {} Probability: {} Iterations: {} Length {}".format(n,p,it,k))
    # Random shots
    sframe=pd.DataFrame(np.random.random_sample((n,it))).\
            applymap(lambda x: x < p)
    logger.info("Shooting simulation done{:%B %d, %Y %H %M %S}".format(datetime.datetime.now()))
    # Assign colours based on shots taken by shooters to the left
    rframe=sframe.apply(
        lambda x:
           [((i>2) and np.all(x.values[i-k:i])) for i in x.index]
    )
    bframe=sframe.apply(
        lambda x:
           [((i>2) and not np.any(x.values[i-k:i])) for i in x.index]
    )
    gframe= ~(rframe | bframe)
    logger.info("Colour assignment done{:%B %d, %Y %H %M %S}".format(datetime.datetime.now()))

    # Mean of probabilities per run
    pframe=pd.Series([0.,0.,0.],index=["Red","Blue","Grey"])
    pframe["Red"]  = np.nanmean((100.0*np.sum(rframe&sframe))/np.sum(rframe)) 
    pframe["Blue"] = np.nanmean((100.0*np.sum(bframe&sframe))/np.sum(bframe))
    pframe["Grey"] = np.nanmean((100.0*np.sum(gframe&sframe))/np.sum(gframe))

    # Mean of probabilities over the ensemble
    tframe=pd.DataFrame([],index=["Red","Blue","Grey","Total"],
                          columns=["shots","hits","percentage"])
    tframe["shots"] = [np.sum(rframe.values),np.sum(bframe.values),
                         np.sum(gframe.values),n*it]
    tframe["hits"]  = [np.sum((rframe&sframe).values),
                         np.sum((bframe&sframe).values),
                         np.sum((gframe&sframe).values),
                         np.sum(sframe.values)]
    tframe["percentage"]= (100.0 * tframe["hits"])/tframe["shots"]

    logger.info("End{:%B %d, %Y %H %M %S}".format(datetime.datetime.now()))
    return pframe,tframe

if __name__ == "__main__":
    def getargs():
        parser = argparse.ArgumentParser(description='Hot Hand Simulator')
        parser.add_argument('--n',type=int,default=12,
                            help="Number of shooters")
        parser.add_argument('--p',type=float,default=0.5,
                            help="Probability of hitting a shot")
        parser.add_argument('--trials',type=int,default=1000,
                            help="Number of trials")
        parser.add_argument('--k',type=int,default=3,
                            help="Required hot hand length")
        parser.add_argument('--prob',action='store_true',
                            help="Generate Probability Plots")
        args=parser.parse_args()
        return args
    
    def main():
        args=getargs()
        if not args.prob:
            logging.basicConfig(filename='hothand.log',
                                filemode='w', level=logging.INFO)
            result=hothand(args.n,args.p,args.k,args.trials)
            print("Per Run:\n",result[0])
            print("Ensemble:\n",result[1])
        else:
            logging.basicConfig(filename='hothand.log',
                                filemode='w', level=logging.WARNING)
            print("Later")
          
    main()
