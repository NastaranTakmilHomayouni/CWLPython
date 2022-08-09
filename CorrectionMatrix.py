import numpy as np
#from progress.bar import Bar
import warnings
from tqdm import trange
from time import sleep
from tkinter import *
from tkinter.ttk import *
import time
#from ProgressBar import Progress
def  CorrectionMatrix( raw, weighting_matrix, Peak_references, onset_value, offset_value):
    '''
    % CorrectionMatrix.m is a function used by Bergen EEG&fMRI Toolbox for
% EEGLAB in order to remove the fMRI artifacts on a EEG dataset recording.
% Using this function, the pointed CURRENTSET of the EEG structure will be
% rewriten after processing and removing the artifacts.
%
% USAGE:
%       [ EEG ] = CorrectionMatrix( EEG, weighting_matrix, Peak_references,
%                 onset_value, offset_value, baseline_matrix);
%
% INPUTS:
%        EEG - is the structure loaded by the EEGLAB. This structure must
%              have a loaded dataset. This function uses internaly the
%              dataset refered as the CURRENTSET.
%
%        weighting_matrix - is a matrix used for correcting EEG data. This
%                           matrix must be quadratic [ M x M ], where M is
%                           the number of artifacts considered for
%                           correction.
%
%        Peak_references - This matrix contains the references of each
%                          start of the fMRI artifact for each independent
%                          EEG dataset channel. It has of
%                          [ channels  x  Nº. of fMRI References found ].
%
%        onset_value - is the position of the real start of each artifact,
%                      relative to the marker position. Must be expressed
%                      in data points. (e.g. -150)
%
%        offset_value - is the position of the real end of each artifact,
%                       relative to the marker position.Must be expressed
%                      in data points. (e.g. +11200)
%
% OUTPUT:
%        EEG - is the structure of data used by EEGLAB. This structure will
%              be rewriten with the corrected EEGdataset.
%
% See also m_rp_info, m_moving_average, m_single_motion, detectchannel,
% detectmarkers, baselinematrix

% Copyright (C) 2009 The Bergen fMRI Group
%    data = raw.get_data()[:,1:10666200]*(10**6)

% Bergen fMRI Group, Department of Biological and Medical Psychology,
% University of Bergen, Norway
%
% Written by Emanuel Neto, 2009
% netoemanuel@gmail.com
%
% Last Modified on 18-Jun-2009 08:07:11'''
    data = raw.get_data()
    lim1 = Peak_references.shape[1]
    lim2 = weighting_matrix.shape[1]
    A = np.zeros(shape=(lim1,offset_value-onset_value+1 ))
    CorrectionM= np.zeros(shape=(lim1,offset_value-onset_value+1 ))
    Correctionmatrix= np.zeros(shape=(lim1,offset_value-onset_value+1 ))
    residual = lim2-lim1+1
    message = ''
    n_channels = len(raw.ch_names)
    step=0
    #tqdm(0, desc='Initializing')
    total=n_channels*lim2*2
    #intro = trange(0,desc='Gradient Correction Initializing', leave=True)
    t = trange(100, desc='Applying Changes', leave=True)
    try:
        for ch in range(1,n_channels+2):
            if ch > n_channels:
                for i in range(residual,lim2+1):
                    step = step+1
                    #Progress(step,total,ch,n_channels)
                    steptostr = str(np.round((step / total) * 100))
                    #t.n=int(np.round((step / total) * 100))
                    #t.set_description("Applying Changes (channel {} / {}) Total Progress {}%" .format(ch,n_channels,steptostr))
                    #t.update()
                    #sleep(0.001)
                    #t.set_description("Applying Changes ( Channel " + str(ch) + "/" + str(n_channels) + ") Total Progress" + steptostr + "%")
                    #with Bar('Applying changes (Channel '+ str(ch)+'/'+str(n_channels)+'). Total progress: ', fill='|', suffix='%(percent).1f%% - %(steptosrt)ds') as bar:
                     #   sleep(0.02)
                      #  bar.next()
                    starter = int(np.fix(Peak_references[0,i-1]+onset_value))
                    ender = int(np.fix(Peak_references[0,i-1]+offset_value))
                    data[ch-2,starter:ender+1]=CorrectionM[i-1,:]

            else:
                for i in range(residual,lim2+1):
                    step = step+1
                    #tqdm(steptosrt, desc='Initializing')
                    #with Bar('Applying changes (Channel '+ str(ch)+'/'+str(n_channels)+'). Total progress: ', fill='|', suffix='%(percent).1f%% - %(steptosrt)ds') as bar:
                        #sleep(0.02)
                        #bar.next()
                    #Progress(step, total, ch, n_channels)
                    #t.set_description("Applying Changes ( Channel " + str(ch) + "/" + str(n_channels) + ") Total Progress" + steptostr + "%")
                    #t.refresh()  # to show immediately the update
                    steptostr = str(np.round((step / total) * 100))
                    t.n = int(np.round((step / total) * 100))
                    t.set_description("Applying Changes (channel {} / {}) Total Progress {}%".format(ch, n_channels, steptostr))
                    t.update()
                    sleep(0.0001)
                    starter = int(np.fix(Peak_references[0,i-1]+onset_value))
                    ender = int(np.fix(Peak_references[0,i-1]+offset_value))
                    A[i-1,:] = data[ch-1,starter:ender+1].T
                    if ch > 1:
                        data[ch-2,starter:ender+1]=CorrectionM[i-1,:]

                for i in range(residual,lim2+1):
                    step = step+1
                    #with Bar('Applying changes (Channel '+ str(ch)+'/'+str(n_channels)+'). Total progress: ', fill='|', suffix='%(percent).1f%% - %(steptosrt)ds') as bar:
                     #   sleep(0.02)
                      #  bar.next()
                    #Progress(step, total, ch, n_channels)
                    steptostr = str(np.round((step / total) * 100))
                    #t.set_description("Applying Changes ( Channel " + str(ch) + "/" + str(n_channels) + ") Total Progress" + steptostr + "%")
                    #t.refresh()  # to show immediately the update
                    t.n = int(np.round((step / total) * 100))
                    t.set_description("Applying Changes (channel {} / {}) Total Progress {}%".format(ch, n_channels, steptostr))
                    t.update()
                    sleep(0.0001)
                    w=weighting_matrix[i-1,:]/np.sum(weighting_matrix[i-1,:])
                    #print(np.sum(weighting_matrix[i-1,:]))
                    w = np.expand_dims(w, axis=0)
                    Correctionmatrix [i-1,:] = np.matmul(w,A)


                CorrectionM= A - Correctionmatrix

        #with Bar('Process completed', fill='|') as bar:
         #   sleep(0.02)
          #  bar.next()
        #t.close()
        #ending = trange(100, desc='Process Completed!', leave=True)
    except:
        message =  """Memory index error. EEG dataset was not modifyed!
                   Possible causes:
                   a) Artifact duration exceedes dataset limit. Please check if last artifacts are complete. It might be necessary to cut dataset.
                   b) Not enough memory. Please read how to handle with Large Datasets in http://www.mathworks.com/support/tech-notes/1100/1107.html"""
        warnings.warn(message)
    return data,message,CorrectionM



