"""
This code implements a three-layer neural network that can be trained
on the XOR or MNIST problem.

It utilizes the mxarr and batch python modules for fast array processing.

This code is supplied for CIS*2750 Fall 2023.  (C) 2023, S.C. Kremer
"""

################################################################################
# standard python modules
import math;    # for sqrt function to calculate L2 norm
import sys;     # to process command line arguments and exit on failure

# custom python modules
import mxarr;
import batch;
import mxarrsql;

################################################################################
# utility functions
def shape( arr ):
  """
  This function returns the shape (size of each dimension) of an array as 
  a tuple.  It is intended of debugging purposes.
  """
  return tuple( [ arr.getdim(i) for i in range( arr.dimno ) ] );

################################################################################
def displayimage( arr, image ):
  """
  This function prints the integer pixel values in a 28x28 grid of one image
  from a flattened array of images (i.e. an array of shape (n,784)).
  The image displayed is indexed by the value of the argument image.
  """
  for i in range(28):
    for j in range(28):
      print( "%3d " % arr.getuchar(image,i*28+j), end="" );
    print();

################################################################################
def displayimagedbl( arr, image ):
  """
  This function prints the double precision pixel values in a 28x28 grid 
  of one image from a flattened array of images (i.e. an array of shape 
  (n,784)).  The image displayed is indexed by the value of the argument image.
  """
  for i in range(28):
    for j in range(28):
      print( "%4.2f " % arr.getdouble(image,i*28+j), end="" );
    print();

################################################################################
def printmatrix( arr, rowno=10, colno=10, total=5, decimals=2 ):
  """
  This function prints a 2 dimensional matrix of either DOUBLE_TYPE or
  UCHAR_TYPE.

  If the number of rows in the matrix exceeds rowno, then the rows are
  elided (with rowno/2 printed before and after the elipsis).

  If the number of columns in the matrix exceeds colno, then the columns are
  elided (with colno/2 printed before and after the elipsis).

  Each floating point value is printed using a %5.2f (C-style) format.
  The total number of digits and the number of digits after the decimal
  can be specified by the total and decimals arguments.

  Each integer value is printed using a %5d (C-style) format.  The
  total number of digits can be specified by the total argument.
  """

  rows = arr.getdim( 0 );   # convenience variable
  cols = arr.getdim( 1 );   # convenience variable

  if arr.type==mxarr.DOUBLE_TYPE:
    fmt = "%%%d.%df " % (total,decimals);
  elif arr.type==mxarr.UCHAR_TYPE:
    fmt = "%%%dd " % (total,);
  else: 
    raise ValueError( "array must be DOUBLE_TYPE or UCHAR_TYPE not %d" % \
            arr.type );


  if rows>rowno:    # too many rows
    # create a list of which columns to display
    rowlist = list(range(rowno//2)) + [". . . "] + \
              list(range(rows-rowno//2,rows));
  else:
    # display them all
    rowlist = range(rows);

  if cols>colno:    # too many columns
    # create a list of which rows to display
    collist = list(range(colno//2)) + [". . . "] + list(range(cols-colno//2,cols));
  else:
    # display them all
    collist = range(cols);

  for i in rowlist:
    # check for elispsis ( . . . ) string
    if type(i) == type(""):
      print( i );
    else:
      for j in collist:
        # check for elipsis ( . . . ) string
        if type(j) == type(""):
          print( j, end="" );
        else:
          print( fmt % arr[ i, j ], end="" );

      print();  # newline at end of row
 
################################################################################

class NN:
  """
  This class respresents a three-layer fully connected perceptron neural 
  network.  It uses logistic activation units in the hidden and output
  layers and is trained with a simple mini-batch gradient descent algorithm 
  (with no momentum).
  """

  def __init__( self, name, ETA, input_scale, hidden_no, batch_size ):
    """
    This constructor creates the newtwork.  
        name is a name given to the networks,
        input_scale is a divisor to convert the input data into values
            between 0 and 1,
        hidden_no is the number of hidden (middle-layer) units in the network
        (the number of input and output units are determined by the dataset),
        batch_size is the size of each training batch.

    This is an abstract base class that should not be instantiated, but
    rather used as a parent class for creating useful subclasses.

    Subclasses must include the following attributes:
        inputs - input patterns
        targets - target pattens
    """
       
    # make sure the base class added inputs and targets to the class definition
    if not hasattr(self,'inputs'):
      raise "Subclass must initialize self.inputs";
    if not hasattr(self,'targets'):
      raise "Subclass must initialize self.targets";

    # transfer arguments to object attributes
    self.name = name;
    self.ETA = ETA;
    self.input_scale = input_scale;
    self.hidden_no = hidden_no;
    self.batch_size = batch_size;

    # set additional information
    self.input_no = self.inputs.getdim( 1 );    # number of input units
    self.output_no = self.targets.getdim( 1 );  # number of output units

    # create input to hidden layer weights
    self.i2h = mxarr.Array( self.input_no*self.hidden_no, mxarr.DOUBLE_TYPE );
    
    self.i2h.inflate( self.input_no );
  
    self.i2h.apply( mxarr.random03 );

    # create hidden bias values
    self.b2h = mxarr.Array( self.hidden_no, mxarr.DOUBLE_TYPE );
    self.b2h.inflate( 1 );
    self.b2h.apply( mxarr.random03 );

    # create hidden to output layer weights
    self.h2o = mxarr.Array( self.hidden_no*self.output_no, mxarr.DOUBLE_TYPE );
    self.h2o.inflate( self.hidden_no );
  
    self.h2o.apply( mxarr.random03 );

    # create output bias values
    self.b2o = mxarr.Array( self.output_no, mxarr.DOUBLE_TYPE );
    self.b2o.inflate( 1 );
    self.b2o.apply( mxarr.random03 );

    # create a set of minibatches for the training data
    self.mbs = batch.MiniBatches( self.inputs, self.targets, self.batch_size, \
                             self.input_scale );



  def train( self, epochs, DEBUG=False, CONFUSION=False ):
    """
    This method trains the NN using mini-batch gradient descent
    for the given range epochs (with no momentum).  ETA is the learning rate
    if DEBUG is true additional printouts will be made.

    If epochs does not begin at zero, then the network parameters are
    loaded from the database.
    """

    fp = open( self.name + ".l2", "w+" );

    if epochs.start!=0:
      self.epoch = epochs.start;
      self.load();

    # loop over epochs
    for self.epoch in epochs:
      sys.stdout.write( "%02d: " % self.epoch );
      # researt the mini-batches (shuffle, start at the beginning)
      self.mbs.restart();

      # while there a minibatches, get the next minibatch 
      while True:
        sys.stdout.write( "." );
        sys.stdout.flush();

        mb = self.mbs.next();
        if mb==None:    # next minimbatch failed
          break;        # exit while loop

        if DEBUG:
          # print all the weights
          print( "i2h" );
          printmatrix( self.i2h, decimals=8 );
          print( "b2h" );
          printmatrix( self.b2h, decimals=8 );
          print( "h2o" );
          printmatrix( self.h2o, decimals=8 );
          print( "b2o" );
          printmatrix( self.b2o, decimals=8 );


        # execute feed forward passfeedforward
        # these are the first two equations on slide 32 of the "NNs F23"
        # power point

        hidden = (mb.inputs ** self.i2h + self.b2h).apply( mxarr.logistic );
        output = ( hidden ** self.h2o + self.b2o).apply( mxarr.logistic );

        # this prints out a confusion matrix of output vs target values
        if CONFUSION:
          # compute confusion matrix
          self.conf = mxarr.matrixconfusion( output.onecold(), \
                                                mb.targets.onecold() );
          print();
          printmatrix( self.conf, rowno=10, colno=10, total=5, decimals=0 );
        # compute errors
        # vector error
        error = output - mb.targets;
        #cumulative error
        fp.write( "%02d.%02d: %f\n" % ( self.epoch, self.mbs.nextbatch-1, \
                math.sqrt( error.copy().apply( mxarr.square ).sum() ) ) );
        fp.flush();

        # backpropagate errors
        # these are the third and fourth equations on slide 32 of the "NNs F23"
        # power point
        outdel = error * (output * (1.0 - output));
        hiddel = outdel ** self.h2o.T() * hidden * (1.0 - hidden);
        if DEBUG:
          print( "inputs" );
          printmatrix( mb.inputs, decimals=2 );
          print( "hidden" );
          printmatrix( hidden, decimals=8 );
          print( "output" );
          printmatrix( output, decimals=9 );
          print( "target" );
          printmatrix( mb.targets, decimals=8 );
          print( "error" );
          printmatrix( error, decimals=8 );
          print( "outdel" );
          printmatrix( outdel, decimals=8 );
          print( "hiddel" );
          printmatrix( hiddel, decimals=8 );

        # update parameters in weights and bias values
        # these are the fifth to eighth equations on slide 32 of the "NNs F23"
        # power point
        self.i2h -= self.ETA * (mb.inputs.T() ** hiddel);
        self.b2h -= self.ETA * hiddel.sumcols();
  
        self.h2o -= self.ETA * (hidden.T() ** outdel);
        self.b2o -= self.ETA * outdel.sumcols();

      sys.stdout.write( "\n" );

      if self.ETA==0.0:
        break;
      # save the network once per epoch
      self.epoch += 1;
      self.save();


    fp.close();

  def save( self ):
    """
    This method saves all network parameters, the latest confusion matrix,
    and a complete history of l2norms to the database.
    """
    batch = self.mbs.nextbatch;         # this method is called at the end of
                                        # the batch

    if batch >= self.mbs.batches:       # check if it was the last batch
      batch = '0';                      # reset batch
      epoch = str( self.epoch+1 );      # increment epoch, because it is also
                                        # done
    else:
      batch = str( batch );
      epoch = str( self.epoch );        # epoch is not done

    db = mxarrsql.Database();
    db.store_arr( self.name + '[' + epoch + ',' + batch + '].i2h',  self.i2h  );
    db.store_arr( self.name + '[' + epoch + ',' + batch + '].b2h',  self.b2h  );
    db.store_arr( self.name + '[' + epoch + ',' + batch + '].h2o',  self.h2o  );
    db.store_arr( self.name + '[' + epoch + ',' + batch + '].b2o',  self.b2o  );
    db.close();

  def load( self ):
    """
    This method loads all network parameters, the latest confusion matrix,
    and a complete history of l2norms from the database.

    Load must be called at the beginning of an epoch, so the batch number
    will be 0.
    """
    epoch = str( self.epoch );

    db = mxarrsql.Database();
    self.i2h = db.retrieve_arr( self.name + '[' + epoch + ',0].i2h' );
    self.b2h = db.retrieve_arr( self.name + '[' + epoch + ',0].b2h' );
    self.h2o = db.retrieve_arr( self.name + '[' + epoch + ',0].h2o' );
    self.b2o = db.retrieve_arr( self.name + '[' + epoch + ',0].b2o' );
    db.close();

class MNIST( NN ):
  """
  This class is a subclass of NN that is designed to process the MNIST
  database.
  """
  def __init__( self, **keywords ):
    """
    Constructor function.

    Load MNIST training data from "train-images-idx3-ubyte",
    flatten the 3d array of 60000x28x28 to a 2d array of
    60000x784, convert to double, and store the data as self.inputs.

    Load MNIS labels data from "train-labels-idx1-ubyte",
    apply onehot encoding, and store the data as self.targets.
    """

    fp = mxarr.fopen( "train-images-idx3-ubyte", "r" );
    if not fp:
        print( "file open failed" );
        sys.exit();
    self.inputs = mxarr.readarray( fp );
    mxarr.fclose( fp );
    self.inputs.flatten();
    self.inputs = self.inputs.todouble();

    fp = mxarr.fopen( "train-labels-idx1-ubyte", "r" );
    if not fp:
        print( "file open failed" );
        sys.exit();
    self.labels = mxarr.readarray( fp );
    self.targets = self.labels.onehot();
    mxarr.fclose( fp );

    keywords['hidden_no'] = 784;        # hidden units match input

    keywords['input_scale'] = 255.0;    # convert input pixels from 0-255
                                        # to 0.0-1.0

    keywords['batch_size'] = 1000;      # size of each mini-batch

    keywords['ETA'] = 0.001;            # learning rate

    NN.__init__( self, **keywords );    # call the parent constructor

class XOR( NN ):
  """
  This is a simple XOR network for testing/debugging purposes.
  """

  def __init__( self, **keywords ):
    """
    self.inputs is a 4x2 array with values 
      [ (0.0,0.0), 
        (0.0,1.0), 
        (1.0,0.0), 
        (1.0,1.0) ]

    self.targets is a 4x1 array with values [ (0.0), (1.0), (1.0), (0.0) ]

    """

    self.inputs = mxarr.Array( 4*2, mxarr.DOUBLE_TYPE );
    self.inputs.inflate(4);
    self.targets = mxarr.Array( 4*1, mxarr.DOUBLE_TYPE );
    self.targets.inflate(4);
    self.inputs[0,0] = 0.0; self.inputs[0,1] = 0.0; self.targets[0,0] = 0.0;
    self.inputs[1,0] = 0.0; self.inputs[1,1] = 1.0; self.targets[1,0] = 1.0;
    self.inputs[2,0] = 1.0; self.inputs[2,1] = 0.0; self.targets[2,0] = 1.0;
    self.inputs[3,0] = 1.0; self.inputs[3,1] = 1.0; self.targets[3,0] = 0.0;

    keywords['hidden_no'] = 2;        # hidden units match input
    keywords['input_scale'] = 1.0;      # no input scaling required
    keywords['batch_size'] = 4;         # each batch is the full dataset
    keywords['ETA'] = 0.5;              # learning rate

    NN.__init__( self, **keywords );    #call the parent constructor

if __name__ == "__main__":
    #xor = XOR( name='xor1' );
    #xor.train( epochs=range(2000) );

    mnist = MNIST( name=sys.argv[1] );
    mnist.train( epochs=range( int(sys.argv[2]), int(sys.argv[3]) ) );

