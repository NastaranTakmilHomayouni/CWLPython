import numpy as np
    #function Y = d
class CustomError(Exception):
    pass
def delay_embed(X, k, step=1, shift=0):
    global Y
    #DELAY_EMBED - Delays-embed a signal
    #Y = delay_embed(x, k, tau, shift)
    #Where
    #K is te embedding dimension
    #TAU is the embedding delay
    #SHIFT is the embedding shift
    #Y is the delay-embedded reconstructed state space, i.e. a KxT matrix
    #See also: misc
    #import misc.isnatural;
    #import misc.isinteger;+++++++++++++++++++++++++++++++++++++++++++++++++++++
    #import misc.delay_embed;
    if k is None and X is None:
        raise('Not enough input arguments')
    #deal with the case of multiple input signals
    if type(X) is list: #X is an ndarray
        Y=list()
        if X.shape[0] and np.size(k) is 1: #X is a one dimensional ndarray like 1 by n
            k=np.tile(k,(X.shape[0],1))
        if X.shape[0] and np.size(shift) is 1:
            shift =np.tile(shift,(X.shape[0],1))
        if X.shape[0] and np.size(step) is 1:
            step = np.tile(step, (X.shape[0],1))
        for i in range(0,X.shape[0]):
            for j in range(0,X.shape[1]):
                Y[i,j]= delay_embed(X[i,j], k[i], step[i], shift[i])
        return

########################################################################################################################
    if not(isinstance(k, int) and 0 <= k):
        raise CustomError('delay_embed:invalidEmbeddingDim The embedding dimension must be a natural number')
    if not(isinstance(shift,int)):
        raise CustomError('delay_embed:invalidEmbedShift',
            'The embedding shift must be an integer number')
    if not(isinstance(step, int) and 0 <= step):
        raise CustomError('delay_embed:invalidTau',
            'The embedding delay must be a natural number')
########################################################################################################################
    n=X.shape[0]
    embedDim = k* n
    embedSampleWidth = (k-1) * step+ 1
    extraSample = shift + embedSampleWidth - 1
    extraSampleL = np.floor(extraSample/2)
    extraSampleR = extraSample - extraSampleL
    X=np.concatenate((X[:,np.arange(int(extraSampleL)-1,-1,-1)],X,X[:,np.arange(X.shape[1]-1,X.shape[1]-1-int(extraSampleR),-1)]),axis=1)
    embed_samples=(X.shape[1] - shift ) - embedSampleWidth + 1
    Y=np.empty([embedDim, embed_samples], dtype=type(X))
    Y[:]=np.nan
    print(X.shape)
    print(Y.shape)
    print(k)
    for j in range(1,k+1):
        s = (shift +step *(j-1)+1)
        print('j = ',j)
        print('s = ',s)
        print('Y[{}:{},:]=X[:,{}:{}]'.format((j - 1) * n, j * n , s - 1, s + embed_samples - 1))
        Y[(j-1)*n:j*n,:]=X[:,s-1:s+embed_samples-1]

    Y = np.flipud(Y)
    return Y