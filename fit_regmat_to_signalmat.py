from my_vector_shifter import my_vector_shifter
from my_pinv import my_pinv
import numpy as np
import my_vector_shifter
from delay_embed import delay_embed

# make this a function that outputs all the desired metrics, also.
#x, the data(n - chan by m - pointsintime)
#regs, the regressors
#window, the window that should be used(m timepoints long!)
#delay_in_samples( if this is set, expand all the regressors to all time
#points for each channel).
#fix_delay, a matrix of nchannels - by - mregressors( if this is set, expand
#regressor m for channel n by matrix(n, m) time points.
#if fix_delay is set, delay_in_samples should be[].
#if delay_in_samples is set, fix_delay should be[].

#function[fittedregs logging] =
def fit_regmat_to_signalmat(x, regs, window, delay_in_samples, fix_delay, do_logging):

    nx=x.shape[0]
    nregs = regs.shape[0] #number of regressors.

    #print(nx,'-',nregs,'-',window.shape,'-',delay_in_samples,'-',fix_delay,'-',do_logging)
    #nit here...
    logging={
        'bparams' : [],
        'corrs' : [],
    }

    #time-expand regressors (only if the delays are not given explicitly in a
    #matrix).
    print(len(fix_delay))
    if len(fix_delay) == 0:
        #full expansion for every channel.
        print(delay_in_samples)
        expregs=np.flipud(delay_embed(regs, int(1+2 * delay_in_samples)))
    # window that...
    # keyboard;
        if len(window) != 0:
            #window=np.round(window,9)
            my_array=np.transpose(expregs)
            #window = np.expand_dims(window, axis=1)
            print('m',my_array.shape)
            print('window size', window.shape)
            expregs = np.transpose( np.multiply(np.matmul(window, np.ones((1, expregs.shape[0]))) ,np.transpose(expregs)))
            print('expregs size', expregs.shape)
        #expregs = (window * ones(1, size(expregs, 1)). * expregs')';


    expregs=expregs.astype('float64')
    #inv_expregs = np.linalg.pinv(expregs)
    inv_expregs = my_pinv(expregs)

    fittedregs = np.zeros(x.shape,dtype=type(x))
    new_key_value_pairs={'fitscale': [],'fitdelay':[],'fitmetric_scale': [],'fitmetric_delay':[]}
    logging.update(new_key_value_pairs)
    #fill that up!
    #this calculation goes for each channel, separately!
    for i_x in range(0,nx):
        if len(window) != 0:
            datavec = np.multiply(x[i_x,:],np.transpose(window))
        else:
            datavec = x[i_x,:]

        if len(fix_delay) !=0:
            if fix_delay.shape[0] is not x.shape[0] or fix_delay.shape[1] is not regs.shape[0]:
                raise('fix_delay should be specified as a matrix of nchan-by-nreg integer values!')

            expregs = np.zeros((regs.shape))
            delay_values = fix_delay[i_x,:]

            for i_reg in range (0,nregs):
                expregs[i_reg,:] = my_vector_shifter(regs[i_reg-1,:],delay_values[i_reg] )
    # window this...
            if len(window) != 0:
                expregs =np.transpose( np.multiply( window * np.ones((1,expregs.shape[0] )) , np.transpose(expregs) ) )


    # and ...also, of course, calculate the pinv!
            inv_expregs = my_pinv(expregs)
            #inv_expregs = np.linalg.pinv(expregs)


    #keyboard;

    #keyboard;
        #print(datavec.shape)
        #print(inv_expregs.shape)
        #print(expregs.shape)
        fitted = np.matmul( np.matmul(datavec , inv_expregs) , expregs)
        print(fittedregs.shape,fitted.shape)
        fittedregs[i_x,:]=fitted

    # log here...
    # dologging = 1;
    # let's do that another(i.e., better) way...
        if do_logging == 1:
    # do it another way...all_beta_params = datavec * inv_expregs;
    # invert only a part(of 1 regressor) this time; not everything!
    #keyboard;
            for i_reg in range(0,nregs):
        # t_expregs = expregs(i_reg:nregs: end,:);
        # inv_t_expregs = pinv(t_expregs);
        # disp(i_x);
        # disp(i_reg);
        # tmp2 = datavec * inv_t_expregs;
        # keyboard; # must think this over...again!
                tmp = datavec * inv_expregs
                logging['bparams'][i_x, i_reg] = tmp[i_reg-1:len(tmp):nregs]

    #keyboard;

            for i_reg in range(0,nregs):
    # correlations!!
    # expregs;
                tmp = expregs[i_reg-1:len(expregs):nregs,:]
        #tcorrs = corr(datavec',tmp')
                tcorrs= np.corrcoef(np.hstack((np.transpose(datavec),np.transpose(tmp))), rowvar=False)[0, 1:]
                logging['corrs'][i_x, i_reg]=tcorrs


    return [fittedregs,logging]