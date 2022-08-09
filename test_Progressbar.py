from tqdm import trange
from time import sleep
import warnings
t = trange(100, desc='Bar desc', leave=True)
i=0
t.set_description("Bar desc (file %i)" % i)
        #t.write(str(2))
        #t.refresh() # to show immediately the update
sleep(0.5)
try:
    for j in range(2):
        for i in range (10):
            t.n=i
            t.set_description("Applying Changes (channel {} / {}) Total Progress {}%".format(i, 76, j))
            t.update()
            sleep(0.5)
        for i in range (9,20):
            t.n=i
            t.set_description("Bar desc (file {}) and {}" .format(2,j)  )
            t.update()
            sleep(0.5)
except:
    message = """Memory index error. EEG dataset was not modifyed!
               Possible causes:
               a) Artifact duration exceedes dataset limit. Please check if last artifacts are complete. It might be necessary to cut dataset.
               b) Not enough memory. Please read how to handle with Large Datasets in http://www.mathworks.com/support/tech-notes/1100/1107.html"""
    warnings.warn(message)
t.close()