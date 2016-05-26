'''
SUMMARY:  Example for mnist classification, using MLP
          Training time: 2 s/epoch. (Tesla M2090)
          Test error: 1.84% after 20 epoches. (Better results can be got by tuning hyper-params)
          Ref: http://deeplearning.net/tutorial/code/logistic_sgd.py
AUTHOR:   Qiuqiang Kong
Created:  2016.05.18
Modified: 2016.05.25 Write annotation
--------------------------------------
'''
import sys
sys.path.append('..')
import numpy as np
np.random.seed(1515)
import pickle
import cPickle
import gzip
import os
from Hat.models import Sequential
from Hat.layers.core import InputLayer, Dense, Dropout
from Hat.callbacks import SaveModel, Validation
from Hat.preprocessing import sparse_to_categorical
from Hat.optimizers import SGD, Rmsprop
import Hat.backend as K

# load data
def load_data():
    dataset = 'mnist.pkl.gz'
    if not os.path.isfile(dataset):
        from six.moves import urllib
        print 'downloading data ... (16.2 Mb)'
        urllib.request.urlretrieve( 'http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz', dataset )
        
    f = gzip.open( dataset, 'rb' )
    train_set, valid_set, test_set = cPickle.load(f)
    [tr_X, tr_y] = train_set
    [va_X, va_y] = valid_set
    [te_X, te_y] = test_set
    f.close()
    return tr_X, tr_y, va_X, va_y, te_X, te_y
   
### load & prepare data
tr_X, tr_y, va_X, va_y, te_X, te_y = load_data()

# init params
n_in = 784
n_hid = 500
n_out = 10

# sparse label to 1-of-K categorical label
tr_y = sparse_to_categorical(tr_y, n_out)
va_y = sparse_to_categorical(va_y, n_out)
te_y = sparse_to_categorical(te_y, n_out)

### Build model
md = Sequential()
md.add( InputLayer( n_in ) )
md.add( Dense( n_hid, act='relu' ) )
md.add( Dropout( p_drop=0.2 ) )
md.add( Dense( n_hid, act='relu' ) )
md.add( Dropout( p_drop=0.2 ) )
md.add( Dense( n_out, act='softmax' ) )

# print summary info of model
md.summary()
md.plot_connection()

### optimization method
#optimizer = SGD( lr=0.01, rho=0.9 )
optimizer = Rmsprop()

### callbacks (optional)
# save model every n epoch (optional)
save_model = SaveModel( dump_fd='Md', call_freq=2 )

# validate model every n epoch (optional)
validation = Validation( tr_x=tr_X, tr_y=tr_y, va_x=None, va_y=None, te_x=te_X, te_y=te_y, metric_types=['categorical_error'], call_freq=1, dump_path='validation.p' )

# callbacks function
callbacks = [validation, save_model]

### train model
md.fit( x=tr_X, y=tr_y, batch_size=500, n_epoch=20, loss_type='categorical_crossentropy', optimizer=optimizer, callbacks=callbacks )

### predict using model
pred_y = md.predict( te_X )

### save model
md.dump( 'mnist_mlp_md.p' )


'''
# Load model
# Later you can use the sentence below to load existing model. (Currently CPU, GPU model can only be loaded using CPU, GPU, respectively)
md = pickle.load( open( 'Md/md2.p', 'rb' ) )
md.fit(...)     # continue training
md.predict(...) # testing
'''