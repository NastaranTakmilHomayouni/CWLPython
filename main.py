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
from mat4py import loadmat
os.chdir(os.path.join(os.getcwd(), 'raw'))
#os.chdir('C:/Users/nasta/PycharmProjects/CWL/data/LernMulti3/raw')
raw_file = os.path.join('fq01_20190618_4.vhdr')
raw = mne.io.read_raw_brainvision(raw_file)
raw = raw.copy().resample(250, npad='auto')
xpicks = mne.pick_channels(raw.info['ch_names'], include=[],exclude=['ECG','CWL1','CWL2','CWL3','CWL4','CWL5','CWL6']) # 69
regpicks = mne.pick_channels(raw.info['ch_names'], include=['CWL1','CWL2','CWL3','CWL4']) #4
xdata, xtimes = raw[xpicks, 0:len(raw.times)] #eegdata is 63 by 11666200
regdata, cwltimes = raw[regpicks, 0:len(raw.times)]  #cwldata is 6 by 11666200
##########################Load Gradient and Baseline Corrected Data#####################################################
os.chdir('C:/Users/nasta/PycharmProjects/CWL/data/LernMulti3/raw_gradient_baseline_corrected')
raw_GBCdata = loadmat('fq01_20190618_4_GBC_resampled_filtered.mat')
raw_GBCdata=np.array(raw_GBCdata['fq01_20190618_4_GBC_resampled_filtered'])
########perform gradient correction#####################################################################################
#octave.addpath('C:/Users/nasta/PycharmProjects/CWLmatlab/eeglab2021.1/plugins/BERGEN1.0/DetectChannel');

#window=np.hanning(len(raw_GBCdata.times))
#window=np.reshape(window,(window.shape[0],1)) #window is 11666200 by 1

#inputdata=raw.get_data()  #inputdata is 69 by 11666200 matrix
inputdata=raw_GBCdata
#Y=fit_regmat_to_signalmat(eegdata, cwldata, window, 9, [], 1)
inputData=Data(inputdata) #inputdata is an object now
regpicks=regpicks
CWLVarargin=Varargin(inputData,regpicks,xpicks) #CWLVarargin is an object containing inputData as an object

#######or######################################
#CWLVarargin=Varargin(inputData) #CWLVarargin is an object containing inputData as a matrix
###############################################
CWLVarargout=run_cwregression(CWLVarargin)
#CWLVarargout=run_cwregression(CWLVarargin)
#np.save('fq01_20190618_4_GBC_CWL.npy', CWLVarargout.outputData)
#subtracted_data=CWLVarargout.outputData.data.subtracted_data
#subtracted_data_weights=CWLVarargout.outputData.data.subtracted_data_weights
#np.save('subtracted_data.npy', subtracted_data)

#chnames=chnames[xpicks]
#chnames=list(chnames)
#TP_raw_info=mne.create_info(chnames, 250.0, verbose=None)
###clean data with MATLAB#######
##################################std####################################################
#os.chdir('C:/Users/nasta/PycharmProjects/CWL/data/LernMulti3/raw_gradient_baseline_cwl_corrected')
#evdata = loadmat('evfq01_20190618_4_GBC_CWL.mat')
#tpdata = loadmat('tpfq01_20190618_4_GBC_CWL.mat')
#sldata = loadmat('slfq01_20190618_4_GBC_CWL.mat')
#evdata=np.array(evdata['fq01_20190618_4_GBC_CWL'])
#tpdata=np.array(tpdata['fq01_20190618_4_GBC_CWL'])
#sldata=np.array(sldata['fq01_20190618_4_GBC_CWL'])
#evdata=evdata[xpicks,:]
#tpdata=tpdata[xpicks,:]
#sldata=sldata[xpicks,:]
###clean data with PYTHON#######EVafter_data,SWafter_data,TPafter_data
#os.chdir('C:/Users/nasta/PycharmProjects/CWL/data/LernMulti3/PythonOutput/Everything')
#EVsubtracted_data=np.load('subtracted_data.npy',allow_pickle=True)
#os.chdir('C:/Users/nasta/PycharmProjects/CWL/data/LernMulti3/PythonOutput/SlidingWindow')
#SWsubtracted_data=np.load('subtracted_data.npy',allow_pickle=True)
#os.chdir('C:/Users/nasta/PycharmProjects/CWL/data/LernMulti3/PythonOutput/TaperedHann')
#TPsubtracted_data=np.load('subtracted_data.npy',allow_pickle=True)
#EVafter_data=raw_GBCdata[xpicks,:]-EVsubtracted_data
#SWafter_data=raw_GBCdata[xpicks,:]-SWsubtracted_data
#TPafter_data=raw_GBCdata[xpicks,:]-TPsubtracted_data
#--------------------------------------------------------------------
#tpstdvalues=np.zeros(shape=(1,69))
#tpsnrvalues=np.zeros(shape=(1,69))
#for i in range(0,68):
 #   tpstdvalues[0,i]=np.std(tpdata[i,:]-TPafter_data[i,:])
  #  tpsnrvalues[0,i]=np.std(TPafter_data[i,:])/tpstdvalues[0,i]
#np.save('tpstdvalues.npy', tpstdvalues)
#np.save('tpsnrvalues.npy', tpsnrvalues)

#evstdvalues=np.zeros(shape=(1,69))
#evsnrvalues=np.zeros(shape=(1,69))
#for i in range(0,68):
 #   evstdvalues[0,i] = np.std(evdata[i, :] - EVafter_data[i, :])
  #  evsnrvalues[0,i] = np.std(EVafter_data[i, :]) /evstdvalues[0,i]
#np.save('evstdvalues.npy', evstdvalues)
#np.save('evsnrvalues.npy', evsnrvalues)

#swstdvalues=np.zeros(shape=(1,69))
#swsnrvalues=np.zeros(shape=(1,69))
#for i in range(0,68):
 #   swstdvalues[0,i] = np.std(sldata[i, :] - SWafter_data[i, :])
 #   swsnrvalues[0,i] = np.std(SWafter_data[i, :]) /swstdvalues[0,i]
 #   np.save('swstdvalues.npy', swstdvalues)
 #   np.save('swsnrvalues.npy', swsnrvalues)

#plt.plot(evdata[5,:], c='red')
#plt.title('method everything , MATLAB , channel 4')
#plt.savefig("everythingMATLABch4.png")

#plt.plot(tpdata[5,:], c='red')
#plt.title('method taperedhann , MATLAB , channel 4')
#plt.savefig("taperedhannMATLABch4.png")

#plt.plot(sldata[5,:], c='red')
#plt.title('method sliding window , MATLAB , channel 4')
#plt.savefig("slidingwindowMATLABch4.png")
#-------------------------------------------------------------------------------------------
#plt.plot(EVafter_data[5,:], c='red')
#plt.title('method everything , PYTHON , channel 4')
#plt.savefig("everythingPYTHONch4.png")

#plt.plot(TPafter_data[5,:], c='red')
#plt.title('method taperedhann , PYTHON , channel 4')
#plt.savefig("taperedhannPYTHONch4.png")

#plt.plot(SWafter_data[5,:], c='red')
#plt.title('method sliding window , PYTHON, channel 4')
#plt.savefig("slidingwindowPYTHONch4.png")

