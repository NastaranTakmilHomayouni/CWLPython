from tkinter import *
from tkinter.ttk import *
import time
from DetectChannel import DetectChannel
from m_moving_average import m_moving_average
from CorrectionMatrix import CorrectionMatrix
from BaselineCorrection import BaselineCorrect
from mat4py import loadmat
#from Data import Data
#from Vararg import Varargin
#from run_cwregression import run_cwregression
import mat4py
#from oct2py import octave
#from fit_regmat_to_signalmat import fit_regmat_to_signalmat
from mat4py import loadmat
import numpy as np
import mne
import matplotlib.pyplot as plt
import os
from Data import Data
from Vararg import Varargin
from run_cwregression import run_cwregression
import mat4py
#from oct2py import octave
from fit_regmat_to_signalmat import fit_regmat_to_signalmat
#os.chdir('C:/Users/nasta/PycharmProjects/CWL/data/LernMulti3/raw')
os.chdir(os.path.join(os.getcwd(), 'raw'))
#scipy.io.savemat("CZraw.mat", {"CZraw": CZraw})
raw_file = os.path.join('fq01_20190618_4.vhdr')
raw = mne.io.read_raw_brainvision(raw_file,preload=False)
events_from_annot, event_dict = mne.events_from_annotations(raw)
#-----perform gradinet correction------------------------------------
Peak_references=events_from_annot[np.where(events_from_annot[:,2]==1128),0]
#---------------------------------------------------------------------------
channel=DetectChannel(raw)
#---------------------------------------------------------------------------
Artifact_onset = 0
Artifact_offset = 10000
#--------------------------------------------------------------------------
weighting_matrix=m_moving_average( Peak_references.shape[1], 20 )
#os.chdir('C:/Users/nasta/PycharmProjects/CWL/data/LernMulti3/raw')
#MATweighting_matrix=np.array(loadmat('weighting_matrix.mat')['weighting_matrix'])
#np.allclose(MATweighting_matrix,weighting_matrix)
#picks=mne.pick_channels(raw.info['ch_names'], include=['Cz'])
#CZ=raw.get_data(picks=picks)
#CZ=CZ[1,34*5000-1:59*5000]
#--------------------------------------------------------------------------
[gradient_corrected_data,message,CorrectionM]=CorrectionMatrix(raw, weighting_matrix, Peak_references, Artifact_onset, Artifact_offset)
#--------------------------------------------------------------------------
gradient_corrected=mne.io.RawArray(gradient_corrected_data,raw.info)
#------gradient correction is done------------------------------------------------------------------------------------------
GBaselineCorrected_data = BaselineCorrect(gradient_corrected, Peak_references, weighting_matrix, 1, Artifact_onset, Artifact_offset, 0, 0, 1)
#--------------------------------------------------------------------------
GBaselineCorrected_raw=mne.io.RawArray(GBaselineCorrected_data,raw.info)
#------baseline correction is done--------------------------------------------------------------------------------------------
BCR_raw=GBaselineCorrected_raw.resample(sfreq=250)
#--------------------------------------------------------------------------
BCRF_raw=BCR_raw.filter(l_freq=1, h_freq=30)
#--------------------------------------------------------------------------
inputdata=BCRF_raw.get_data()
xpicks = mne.pick_channels(BCRF_raw.info['ch_names'], include=[],exclude=['ECG','CWL1','CWL2','CWL3','CWL4','CWL5','CWL6']) # 69
regpicks = mne.pick_channels(BCRF_raw.info['ch_names'], include=['CWL1','CWL2','CWL3','CWL4']) #4
inputData=Data(inputdata)
CWLVarargin=Varargin(inputData,regpicks,xpicks)
CWLVarargout=run_cwregression(CWLVarargin)
