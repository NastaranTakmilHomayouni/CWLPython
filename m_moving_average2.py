#m_moving_average.m is used as part of the Bergen EEG&fMRI Toolbox
# plugin for EEGLAB.

# Copyright (C) 2009 The Bergen fMRI Group
# Bergen fMRI Group, Department of Biological and Medical Psychology,
# University of Bergen, Norway
# Written by Matthias Moosmann, 2009
# moosmann@gmail.com
#Last Modified on 18-Jun-2009 08:07:11
import numpy as np
def m_moving_average (n_fmri,k):
    '''Code to generate weighting matrices for artifact correction with the
    moving average algorithm (Allen et al. Neuroimage 2000)
    n_fmri   - number of fMRI volumes recorded
    k        - number of artifacts that constitute the templates (typical k=25)
    '''
    slid_win=np.zeros((n_fmri,k))     #init sliding slid_win output
    distance=np.zeros((1,n_fmri))     #init linear weights
    for jslide in range(1,n_fmri+1):                             # 'center' of sliding slid_win
        distance[0,0:jslide]=[x for x in range(jslide,0,-1)]     #generate (linear) distance ->
        distance[0, jslide:]=[x for x in range(2,n_fmri-jslide+1,1)]   #triangular plot with smallest values around jslide
    # picking k samples with the smallest distance would now result in standard sliding average
    # next, the motion data is added to this linear distance
        sort_order= distance.argsort(axis=0)  #order sample by distance
        distance.sort(axis=0)  # sort distance in ascending fashion
        sorted_distance=distance
        slid_win[jslide-1, :] = sort_order[1,k] #set sliding slid_win to smallest distance values


    # Create Weighting Matrix
    weighting_matrix = np.zeros((n_fmri, n_fmri))
    for j in range (1,n_fmri+1):
        weighting_matrix[j-1,slid_win[j-1,:]+1]=1

    return weighting_matrix


