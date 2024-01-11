import sys;

import mxarr;
import mxarrsql;
import NN;

class MNIST_Test( NN.NN ):

  def __init__( self, **keywords ):
    """
    constructor function - modelled after the MNIST constructor in NN

    It uses the test files instead of the training files,
    does everything in one batch (no minibatch),
    and has a learning rate of zero.
    """

    fp = mxarr.fopen( "t10k-images-idx3-ubyte", "r" );
    if not fp:
        print( "file open failed" );
        sys.exit();
    self.inputs = mxarr.readarray( fp );
    mxarr.fclose( fp );
    self.inputs.flatten();
    self.inputs = self.inputs.todouble();

    fp = mxarr.fopen( "t10k-labels-idx1-ubyte", "r" );
    if not fp:
        print( "file open failed" );
        sys.exit();
    self.labels = mxarr.readarray( fp );
    self.targets = self.labels.onehot();
    mxarr.fclose( fp );

    keywords['hidden_no'] = 784;        # hidden units match input

    keywords['input_scale'] = 255.0;    # convert input pixels from 0-255
                                        # to 0.0-1.0

    keywords['batch_size'] = 10000;      # size of each mini-batch

    keywords['ETA'] = 0.0;            # learning rate

    NN.NN.__init__( self, **keywords );    # call the parent constructor


if __name__ == "__main__":
  mnist = MNIST_Test( name='sck_mnist_40_0' );
  mnist.train( epochs=range( 40, 41 ), CONFUSION=True );

"""
 0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00
 1.00 1102.00  4.00  0.00  3.00  2.00  3.00 16.00  6.00 10.00
124.00  3.00 903.00 26.00  4.00  8.00  5.00 25.00  6.00 14.00
50.00  3.00 20.00 901.00  2.00 29.00  2.00  8.00 15.00 34.00
 3.00  1.00 16.00  1.00 940.00 24.00  9.00 11.00 14.00 429.00
365.00  0.00  2.00 29.00  1.00 751.00 18.00  1.00 20.00 83.00
205.00  5.00 18.00  7.00 15.00 20.00 913.00  2.00 12.00 10.00
79.00  2.00 26.00 19.00  1.00 14.00  4.00 960.00 16.00 270.00
153.00 19.00 43.00 27.00 16.00 44.00  4.00  5.00 885.00 159.00
 0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00
"""

