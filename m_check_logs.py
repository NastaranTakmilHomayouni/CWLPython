from oct2py import octave
import matplotlib.pyplot as plt
import numpy as np
import imagesc as imagesc
EEG = octave.pop_loadset('filename', 'example_set.set', 'filepath',
                  '/data1/Dropbox/Dropbox/Prog/GitWork/CWRegr/eeglab13_1_1b/plugins/CWRegrTool/example_dataset/')
EEG = octave.pop_cwregression(EEG, 500, 4.000000, 0.050000, 4, 'hann', [33,34,35,36,37,38,39,40],
                       [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
                       'taperedhann', 0)
logs = EEG.cwregression.cfg.cwregression.logging
collect = []
channel = 25
for i_reg in range(1,len([33,34,35,36,37,38,39,40])+1):
    for i in range(1,len(logs)):
        collect[:, i, i_reg] = [logs(i).bparams [channel, i_reg ]]

fig,axs= plt.subplots(3,3)
for i_reg in range(1,9):
    axs[i_reg].imagesc(collect[:,:, i_reg])
    axs[i_reg].title(['cw ' ,str(i_reg)])
    axs[i_reg].set_clim(-0.2,0.2)

axs[9].set_clim(-0.2,0.2)
w = axs[9].get_xaxis()
w.set_visible(False)

plt.colorbar()


collect = []
channel = 25
for i_reg in range(1,len([33,34,35,36,37,38,39,40])+1):
    for i in range(1,len(logs)):
        collect[:, i, i_reg] = np.transpose([logs [i ].corrs [channel, i_reg ]])


fig,axs= plt.subplots(3,3)
for i_reg in range(1,9):
    axs[i_reg].imagesc(collect[:,:, i_reg])
    axs[i_reg].title(['cw ' ,str(i_reg)])
    axs[i_reg].set_clim(-0.9,0.9)

axs[9].set_clim(-0.9,0.9)
w = axs[9].get_xaxis()
w.set_visible(False)
plt.colorbar()


plt.xlabel('window')
plt.ylabel('beta fit parameter')




