/* batch.h
 * minibatch library for C.
 * This library support mini-batch management for neural networks.
 * Created for CIS*2750, by S.C. Kremer, (C) 2023
 */

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

/******************************************************************************/
/* structure for minibatches                                                  */
typedef struct
{
  Array *inputs;              /* 2-d array that is the source of the data */
  Array *targets;	      /* 2-d array that is the target values */
  unsigned int patterns;      /* total number of patterns (arr->dims[0]) */
  unsigned int batchsize;     /* patterns per batch (except the last one) */
  double scaledown;           /* divisor for converting UCHAR to DOUBLE */
  unsigned int batches;       /* total number of batches */
  unsigned int nextbatch;     /* current batch number */
  unsigned int *order;	      /* order of all patterns (across all batches) */
} MiniBatches;

/******************************************************************************/
/* structure for one minibatch                                                */
typedef struct
{
  Array *inputs;	/* 2-d input data matrix */
  Array *targets;	/* 2-d target values matrix */
} MiniBatch;

/******************************************************************************/
/* function prototypes                                                        */


MiniBatches *newminibatches( Array *inputs, Array *targets,
                             unsigned int batchsize, double scaledown );

unsigned int randrange( unsigned int min, unsigned int max );


void shuffle( MiniBatches *minibatches_ptr );
void restartminibatches( MiniBatches *mbs );
MiniBatch *newminibatch( MiniBatches *mbs, unsigned int batchsize );
MiniBatch *nextminibatch( MiniBatches *minibatches_ptr );

void freeminibatches( MiniBatches *minibatches_ptr );
void freeminibatch( MiniBatch *mb );
