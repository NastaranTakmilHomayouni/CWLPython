#m_moving_average.m is used as part of the Bergen EEG&fMRI Toolbox
# plugin for EEGLAB.

# Copyright (C) 2009 The Bergen fMRI Group
# Bergen fMRI Group, Department of Biological and Medical Psychology,
# University of Bergen, Norway
# Written by Matthias Moosmann, 2009
# moosmann@gmail.com
#Last Modified on 18-Jun-2009 08:07:11
import numpy as np
from my_sort import my_sort
def m_moving_average(n_fmri,k):
    '''Code to generate weighting matrices for artifact correction with the
    moving average algorithm (Allen et al. Neuroimage 2000)
    n_fmri   - number of fMRI volumes recorded
    k        - number of artifacts that constitute the templates (typical k=25)
    '''
    # Create Weighting Matrix
    weighting_matrix = np.zeros(shape=(n_fmri, n_fmri))

    slid_win=np.zeros(shape=(n_fmri,k))     #init sliding slid_win output
    distance=np.zeros(shape=(1,n_fmri))     #init linear weights
    for jslide in range(1,n_fmri+1):           # 'center' of sliding slid_win from 1 to n_fmri
        print(jslide)
        distance[0,0:jslide]=np.arange(jslide,0,-1) #generate (linear) distance ->
        distance[0,jslide:]=np.arange(2,n_fmri-jslide+2,1)   #triangular plot with smallest values around jslide

    # picking k samples with the smallest distance would now result in standard sliding average
    # next, the motion data is added to this linear distance
        #sort_order= distance.argsort(axis=1)  #order sample by distance
        sort_order = my_sort(distance)
        #distance.sort(axis=0)  # sort distance in ascending fashion
        #sorted_distance=distance
        slid_win[jslide-1, :] = sort_order[0:k]  #set sliding slid_win to smallest distance values
        weighting_matrix[jslide-1, sort_order[0:k]] = 1



    return weighting_matrix

