/******************************************************************************/
/* File:  batch.i                                                             */
/******************************************************************************/
/* (C) Stefan C. Kremer, 2023                                                 */
/* A swig file to interface Python with the batch library used for CIS*2750,  */
/* Fall 2023.                                                                 */
/******************************************************************************/

/* based on batch.c and batch.h */
%module batch
%{
  #include "mxarr.h"
  #include "batch.h"
%}

/******************************************************************************/

%include "batch.h"

/* include C's fopen and fclose functions, so support C file-io */

%extend MiniBatches {

  /****************************************************************************/
  MiniBatches( Array *input, Array *output, unsigned int batch_size,
               double scaledown )
  {
    MiniBatches *nmb;
    nmb = newminibatches( input, output, batch_size, scaledown );
    if (!nmb)
    {
      PyErr_SetString( PyExc_ValueError, ERROR_STRING );
      return NULL;
    }
    return nmb;
  }

  void restart()
  {
    restartminibatches( $self );
  }

  /****************************************************************************/
  MiniBatch *next()
  /* implementing python iterator functions so it is possible to just loop */
  {
    return nextminibatch( $self );
  }


  /****************************************************************************/
  MiniBatches *__iter__()
  {
    restartminibatches( $self );
    return $self;
  }

  /****************************************************************************/
  MiniBatch *__next__()
  {
    MiniBatch *nextmb;
    nextmb =  nextminibatch( $self );
    return nextmb;
  }

  /****************************************************************************/
  ~MiniBatches()
  {
    freeminibatches( $self );
  }

};

/******************************************************************************/
%extend MiniBatch {
  ~MiniBatch()
  {
    freeminibatch( $self );
  }

}
