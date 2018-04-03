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


def hothand(n=100,p=.5,iter=1000):
    # Random shots
    sframe=pd.DataFrame(np.random.random_sample((n,iter))).\
            applymap(lambda x: x < p)
    print("Shooting simulation done",datetime.datetime.now())
    # Assign colours based on shots taken by shooters to the left
    rframe=sframe.apply(
        lambda x:
           [((i>2) and x[i-1] and x[i-2] and x[i-3]) for i in x.index]
    )
    bframe=sframe.apply(
        lambda x:
           [(i>2) and not (x[i-1] or x[i-2] or x[i-3]) for i in x.index]
    )
    gframe= ~(rframe | bframe)
    print("Colour assignment done",datetime.datetime.now())

    # Mean of probabilities per run
    pframe=pd.Series([0.,0.,0.],index=["Red","Blue","Grey"])
    pframe["Red"]  = np.nanmean((100.0*np.sum(rframe&sframe))/np.sum(rframe)) 
    pframe["Blue"] = np.nanmean((100.0*np.sum(bframe&sframe))/np.sum(bframe))
    pframe["Grey"] = np.nanmean((100.0*np.sum(gframe&sframe))/np.sum(gframe))

    # Mean of probabilities over the ensemble
    tframe=pd.DataFrame([],index=["Red","Blue","Grey","Total"],
                          columns=["shots","hits","percentage"])
    tframe["shots"] = [np.sum(rframe.values),np.sum(bframe.values),
                         np.sum(gframe.values),n*iter]
    tframe["hits"]  = [np.sum((rframe&sframe).values),
                         np.sum((bframe&sframe).values),
                         np.sum((gframe&sframe).values),
                         np.sum(sframe.values)]
    tframe["percentage"]= (100.0 * tframe["hits"])/tframe["shots"]

    print("End",datetime.datetime.now())
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
        args=parser.parse_args()
        return args
    
    def main():
        args=getargs()
        result=hothand(args.n,args.p,args.trials)
        print("Per Run:\n",result[0])
        print("Ensemble:\n",result[1])
    main()
