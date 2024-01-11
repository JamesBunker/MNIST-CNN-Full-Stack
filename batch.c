/* batch.c
 * minibatch library for C.
 * This library support mini-batch management for neural networks.
 * Created for CIS*2750, by S.C. Kremer, (C) 2023
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "mxarr.h"
#include "batch.h"


/******************************************************************************/

MiniBatches *newminibatches( Array *inputs, Array *targets, 
                             unsigned int batchsize, double scaledown )
/*
 * This function creates a MiniBatches structure with the given number of 
 * elements
 * inputs - array of input patterns (unsigned char)
 * utputs - array of target values (unsigned char)
 */
{
  MiniBatches *mbs;

  if (inputs->type!=DOUBLE_TYPE)
  {
    ERROR_CODE = ERR_VALUE;
    sprintf( ERROR_STRING, "newminibatches - bad input data\n" );
    return NULL;
  }

  if (targets->type!=DOUBLE_TYPE)
  {
    ERROR_CODE = ERR_VALUE;
    sprintf( ERROR_STRING, "newminibatches - bad output data\n" );
    return NULL;
  }

  mbs = (MiniBatches *)malloc( sizeof( MiniBatches ) );
  if (!mbs)
  {
    ERROR_CODE = ERR_MEMORY;
    sprintf( ERROR_STRING, "newminibatches - error; out of memory\n" );
    return NULL;
  }

  mbs->inputs = inputs;
  mbs->targets = targets;
  mbs->patterns = mbs->inputs->dims[0];
  mbs->batchsize = batchsize;
  mbs->scaledown = scaledown;
  mbs->batches = mbs->patterns / batchsize +
                             ((mbs->patterns % batchsize) > 1);
  mbs->nextbatch = 0;

  mbs->order = (unsigned int *)malloc( sizeof(unsigned int) * 
      mbs->patterns );

  if (!mbs->order)
  {
    ERROR_CODE = ERR_MEMORY;
    sprintf( ERROR_STRING, "newminibatches - error; out of memory\n" );
    return NULL;
  }

  /* create an array that orders the patterns
   * initialize it to have the patterns in original order:
   *    0, 1, ... , mbs->patterns
   */
  for (int i=0;i<mbs->patterns;i++)
  {
    mbs->order[i] = i;
  }

  //shuffle( mbs );
  return mbs;
}

/******************************************************************************/

unsigned int randrange( unsigned int min, unsigned int max )
/* return a random integer uniformy distributed between min (inclusive)
 * and max (exclusive)
 */
{
  return rand() % (max-min) + min;
}

/******************************************************************************/

void shuffle( MiniBatches *mbs )
/* this function randomly shuffles the contents of the order array within
 * the minibatches structure
 */
{
  for (unsigned int i=0;i<mbs->patterns;i++)
  {
    unsigned int tmp, j;
    j = randrange( i, mbs->patterns );

    /* swap i and j */
    tmp = mbs->order[i];
    mbs->order[i] = mbs->order[j];
    mbs->order[j] = tmp;
  }


}

/******************************************************************************/

void restartminibatches( MiniBatches *mbs )
/* set the current batch to zero and shuffle the minibatches
 */
{
  mbs->nextbatch = 0;
  shuffle( mbs );
}


/******************************************************************************/

MiniBatch *newminibatch( MiniBatches *mbs, unsigned int batchsize )
{
/* create minibatch consisting of a new array of inputs and targets
 * input array will be a double array created from from unsigned char 
 * based on scaledown
 * NOTE:  batchsize may be smaller than mbs->batchsize for the final
 * batch.
 */
  MiniBatch *mb;
  unsigned int iwidth, twidth; // width of input and target vectors

  /* if there are no batches left to provide reset nextbatch to zero
   * (to start again) and return NULL
   */
  if (mbs->nextbatch >= mbs->batches)
  {
    mbs->nextbatch = 0;
    return NULL;
  }

  // conveniece variable
  iwidth = mbs->inputs->dims[1];

  // allocate memory for new MiniBatch 
  mb = malloc( sizeof( MiniBatch ) );
  if (!mb)
  {
    sprintf( ERROR_STRING, "newminibatch - malloc failure\n" );
    ERROR_CODE = ERR_MEMORY;
    return NULL;
  }

  // create input matrix within minibatch
  mb->inputs = newarray( batchsize*iwidth, DOUBLE_TYPE );

  if (!mb->inputs)
  {
    free( mb );
    sprintf( ERROR_STRING, "newminibatch - malloc failure\n" );
    ERROR_CODE = ERR_MEMORY;
    return NULL;
  }

  if (!inflatearray( mb->inputs, batchsize ))
  {
    freearray( mb->inputs );
    return NULL;
  }

  // convenince variable
  twidth = mbs->targets->dims[1];

  // create target matrix within minibatch
  mb->targets = newarray( batchsize*twidth, DOUBLE_TYPE );
  if (!mb->targets)
  {
    free( mb->inputs );
    free( mb );
    sprintf( ERROR_STRING, "newminibatch - malloc failure\n" );
    ERROR_CODE = ERR_MEMORY;
    return NULL;
  }

  if (!inflatearray( mb->targets, batchsize ))
  {
    freearray( mb->targets );
    freearray( mb->inputs );
    free( mb );
    return NULL;
  }

  /* copy shuffled data into input array */
  for (int i=0;i<batchsize;i++)  // for each pattern (row)
  {
    // figure out where to get the pattern based on the order
    unsigned int index = mbs->order[mbs->nextbatch*batchsize+i];

    // copy all columns of the pattern
    for (int j=0;j<iwidth;j++)
    {
      *matrixgetdouble( mb->inputs, i, j ) = 
	  *matrixgetdouble( mbs->inputs, index, j ) / mbs->scaledown; 
      // copy and scale
    }

    // copy all columns of the pattern
    for (int j=0;j<twidth;j++)
    {
      *matrixgetdouble( mb->targets, i, j ) =
	  *matrixgetdouble( mbs->targets, index, j );
      // copy no scale
    }

  }

  /* increment nextbatch */
  mbs->nextbatch++;
  
  /* return array */
  return mb;
}

/******************************************************************************/

MiniBatch *nextminibatch( MiniBatches *mbs )
  /* this function returns the next minibatch from the set of minibatches.
   */
{
  unsigned int batchsize;
  MiniBatch *mb;

  // check if it is the last minibatch
  if (mbs->nextbatch==mbs->batches-1) /* last batch */
  {
    // check how much data is left; might not be a complete batchsize
    batchsize = mbs->patterns % mbs->batchsize; /* remainder */
    if (batchsize==0)
      batchsize = mbs->batchsize;
  }
  else
    batchsize = mbs->batchsize;


  /* create the output array of appropriate size and dimensions */
  mb = newminibatch( mbs, batchsize );


  return mb;
}
/******************************************************************************/

void freeminibatches( MiniBatches *mbs )
  /* free minibatches set */
{
  free( mbs->order );
  free( mbs );
}


/******************************************************************************/

void freeminibatch( MiniBatch *mb )
  /* free individual minibatch */
{
  freearray( mb->inputs );
  freearray( mb->targets );
  free( mb );
}
