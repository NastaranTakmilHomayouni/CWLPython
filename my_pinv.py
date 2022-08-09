import numpy as np
import torch
def my_pinv(x):
    #Mat = torch.tensor(x)
    U, D, VT = np.linalg.svd(x,full_matrices=False)
    #U, D, VT = torch.linalg.svd(Mat)
    VT = VT.T
    max_valu = max(np.abs(D.T))
    max_valu = max_valu.astype('float32')  #to make it single as in matlab
    tol = max(x.shape) * np.spacing(max_valu)
    r1 = sum(D > tol) + 1 # eg r1=45
    V = VT[:,:r1-1] # 0 to 43
    U = U[:,:r1 - 1]
    D = D[:r1 - 1]
    D=np.divide(1, D)
    #VT is 501,44 D.T is 1,44 U.T is 44,100
    X=(np.multiply(V,D.T))@(U.T) #X is 501 by 100
    return X