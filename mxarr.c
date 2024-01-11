#include "mxarr.h"

#include <stdbool.h>

//ERROR_CODE and ERROR_STRING global variables
ERROR_CODES ERROR_CODE;
char ERROR_STRING[256];

/******************************************************************************/
/* Assignment 1 Function Prototypes - C Library to support arrays of up to 4 dimensions with a variety of data types*/
/******************************************************************************/
/*
  dimno - total number of dimensions of array, from 1 to MAX_DIMS
  type -  data type stored in each element in the array, selected from ELEMENT_TYPES enum
  dims -  array of 32 bit unsigned integers storing the size of each dimension in the array, can hold MAX_DIMS values (indicies >= to dimno are not used)
  elno -  total number of elements in entire array, product of elements of dims from 0 to dimno-1
  data -  unsigned char pointer to the location of the data in the array, dynamically allocated when array is created, allocated bytes is elno*ELEMENT_SIZE(type)
*/
Array * conv(Array * arr, Array * conv) {
  return arr;
}

void freearray(Array * arr) {
  //freeing data
  free(arr -> data);

  //freeing struct
  free(arr);
}
/* free array and data*/

void endswap(unsigned char bytes, void * input, void * output) {

  //different place in memory
  if (input != output) {
    //iterating through bytes and reversing bytes
    for (int i = 0; i < bytes; i++) {
      ((char * ) output)[bytes - 1 - i] = ((char * ) input)[i];
    }
  }
  //same place in memory, reversing in place
  else {
    char temp;
    //iterating through bytes and reversing bytes by first storing value to be overwritten to a temp variable
    for (int i = 0; i < bytes / 2; i++) {
      temp = ((char * ) input)[i];
      ((char * ) input)[i] = ((char * ) input)[bytes - 1 - i];
      ((char * ) input)[bytes - 1 - i] = temp;
    }
  }
}
/* reverse the order of the bytes pointed to 'input' and store them in 'output' */

Array * newarray(uint32_t dim0, ELEMENT_TYPES type) {
  //allocate memory for struct
  Array * arr = malloc(sizeof(Array));

  //memory allocation failed
  if (arr == NULL) {
    ERROR_CODE = ERR_MEMORY;
    strcpy(ERROR_STRING, "newarray – malloc failed\n");
    return NULL;
  }

  //allocate memory for data pointer
  arr -> data = malloc(ELEMENT_SIZE(type) * dim0);

  //memory allocation failed
  if (arr -> data == NULL) {
    ERROR_CODE = ERR_MEMORY;
    strcpy(ERROR_STRING, "newarray – malloc failed\n");
    free(arr);
    return NULL;
  }

  //setting struct members based on parameter dim0 and type
  arr -> dimno = 1;
  arr -> dims[0] = dim0;
  arr -> elno = arr -> dims[0];
  arr -> type = type;

  return arr;
}
/* allocate a new Array structure and its data. one dimensional with size of 'dim0' of type 'type' */

unsigned char inflatearray(Array * arr, uint32_t dim) {
  //number of dimensions in arr must be less than the MAX_DIMS and dim[0] must be divisible by dim
  if (((arr -> dims[arr -> dimno - 1] % dim) != 0) || (arr -> dimno == MAX_DIMS)) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "inflatearray – dimensionality error\n");
    return 0;
  }

  //setting new final dim to previous dim / dim
  arr -> dims[arr -> dimno] = arr -> dims[arr -> dimno - 1] / dim;

  //setting previously final dimension to dim
  arr -> dims[arr -> dimno - 1] = dim;

  //increasing dimensions in use by one (not indexes so when used in referencing indexes must reduce number by 1)
  arr -> dimno += 1;

  return 1;
}
/* increase the dimensions of the array, 'arr', by 1 */

void flatten(Array * arr) {
  if (arr -> dimno < 2) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "flatten – dimensionality error\n");
  }

  //setting new final dim to previous dim * removed dim
  arr -> dims[arr -> dimno - 2] = arr -> dims[arr -> dimno - 2] * arr -> dims[arr -> dimno - 1];

  //reseting last dimension to 0
  arr -> dims[arr -> dimno - 1] = 0;

  //decreasing dimensions in use by one
  arr -> dimno -= 1;

}
/* reverse the inflatearray operation */

Array * readarray(FILE * fp) {
  unsigned char magicBytes[4];

  if (fread(magicBytes, 1, 4, fp) != 4) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "readarray – fread error");    
    return NULL;
  }

  bool bigEndian = false;
  bool littleEndian = false;
  int dimno = -1;
  ELEMENT_TYPES type;

  if (magicBytes[0] == 0 && magicBytes[1] == 0) {
    bigEndian = true;
    dimno = magicBytes[3];
    type = (ELEMENT_TYPES) magicBytes[2];
  }

  if (magicBytes[2] == 0 && magicBytes[3] == 0) {
    littleEndian = true;
    dimno = magicBytes[0];
    type = (ELEMENT_TYPES) magicBytes[1];
  }

  if (bigEndian == false && littleEndian == false) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "readarray - file format violation\n");
    return NULL;
  }

  if (dimno > MAX_DIMS) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "readarray - dimensionality error\n");
    return NULL;
  }

  uint32_t dims[MAX_DIMS];
  uint32_t elno = 1;

  for (int i = 0; i < dimno; i++) {
    if (fread( & dims[i], sizeof(uint32_t), 1, fp) != 1) {
      ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "readarray - fread error\n");
      return NULL;
    }
    if (bigEndian == true) {
      endswap(4, & dims[i], & dims[i]);
    }

    elno = elno * dims[i];
  }

  Array * arr = newarray(elno, type);
  if (arr == NULL) {
    return NULL;
  }

  for (int i = 0; i < dimno - 1; i++) {
    inflatearray(arr, dims[i]);
  }

  if (fread(arr -> data, ELEMENT_SIZE(type), elno, fp) != elno) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "readarray - fread error\n");
    freearray(arr);
    return NULL;
  }

  return (arr);
}
/* read an array from a file and return the array */


int writearray(FILE * fp, unsigned char bigendian, Array * arr) {

  // writing magic bytes based on endianess
  unsigned char magicBytes[4];
  if (bigendian != 1) {
    magicBytes[0] = (unsigned char) arr -> dimno;
    magicBytes[1] = (unsigned char) arr -> type;
    magicBytes[2] = 0;
    magicBytes[3] = 0;
  } else {
    magicBytes[0] = 0;
    magicBytes[1] = 0;
    magicBytes[2] = (unsigned char) arr -> type;
    magicBytes[3] = (unsigned char) arr -> dimno;
  }

  if (fwrite(magicBytes, 1, 4, fp) != 4) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "writearray - write error\n");
    return 0;
  }

  // Write the types value to the file
  if (fwrite( & arr -> type, sizeof(ELEMENT_TYPES), 1, fp) != 1) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "writearray - write error\n");
    return 0;
  }

  // Write the dimno value to the file
  if (fwrite( & arr -> dimno, sizeof(int), 1, fp) != 1) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "writearray - write error\n");
    return 0;
  }

  // Write the dimensions to the file endswapped for endianess
  for (int i = 0; i < arr -> dimno; i++) {
    uint32_t dim = arr -> dims[i];
    if (bigendian == 1) {
      endswap(4, & dim, & dim);
    }
    if (fwrite( & dim, sizeof(uint32_t), 1, fp) != 1) {
      ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "writearray - write error\n");
      return 0;
    }
  }

  // Write the array data to the file
  if (fwrite(arr -> data, ELEMENT_SIZE(arr -> type), arr -> elno, fp) != arr -> elno) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "writearray - write error\n");
    return 0;
  }

  return 1;
}
/* opposite of readarray*/


/******************************************************************************/
/* Assignment 1 Function Prototypes - Matrix Algebra Operations*/
/******************************************************************************/
/* Element Modifer Functions */
void random03(double * x) {
  //setting the pointer value to a random value between -0.3 and 0.3
  * x = (((double) rand() * (MAX_RAND - MIN_RAND)) / (double) RAND_MAX) + MIN_RAND;
}
/*replace the value at 'x' by a value that is randomly selected from the uniform distribution between -0.3 and +0.3 */

void logistic(double * x) {
  //setting the pointer value to the 1/(1+e^(-*x)) of the passed argument
  * x = 1.0 / (1.0 + exp(-( * x)));
}
/* replace the value at 'x' by 1/(1+e^(-*x)) */

void square(double * x) {
  //setting the pointer value to the square of the passed argument
  * x = ( * x) * ( * x);
}
/* replace the value at x by the square of the value at x */

/* Matricies and Vectors */
unsigned char ismatrix(Array * arr) {
  //array type must be double
  if (ELEMENT_SIZE(arr -> type) == 8) {
    //array mmust have 2 dimensions
    if (arr -> dimno == 2) {
      return 1;
    }
  }
  return 0;
}
/* return a value of 1 if the array pointed to by arr is a matrix, and 0 otherwise */

unsigned char isvector(Array * arr) {
  //array must be matrix
  if (ismatrix(arr)) {
    //array must have first dimension of size 0
    if (arr -> dims[0] == 1) {
      return 1;
    }
  }
  return 0;
}
/* return a value of 1 if the array pointed to by arr is a vector, and 0 otherwise */

Array * apply(Array * arr, void( * fn)(double * )) {
  //iterates through data blocks in memory by element type size
  for (int i = 0; i < arr -> elno; i++) {
    double * val = (double * )(arr -> data + i * ELEMENT_SIZE(arr -> type));
    //runs data block values through passed function
    fn(val);
  }

  return arr;
}
/* apply an element modifier function (see above) to each element of the array pointed to by arr. 
The function to be applied will be pointed to by the function pointer 'fn' */

Array * copy(Array * arr) {
  //creating new array with size and type of arr
  Array * arrcpy = newarray(arr -> elno, arr -> type);

  //setting dimno
  arrcpy -> dimno = arr -> dimno;

  //inflating array based on arr dims
  for (int i = 0; i < arr -> dimno; i++) {
    arrcpy -> dims[i] = arr -> dims[i];
  }
  //iterating through data and setting copy value to original
  memcpy(arrcpy -> data, arr -> data, arr -> elno * ELEMENT_SIZE(arr -> type));

  return arrcpy;
}
/* return a pointer to a new Array that is an exact (deep) copy of the array pointed to by arr */

double * matrixgetdouble(Array * matrix, unsigned int i, unsigned int j) {
  //matrix must be 2d and of type doubless
  if (matrix -> dimno != 2 || ELEMENT_SIZE(matrix -> type) != 8 || matrix -> elno < 1) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixgetdouble – invalid array\n");
    return NULL;
  }
  //returning point in data memory block by translating dimensions and type to a memory address
  //printf("||%d||", (matrix->dims[1]*j + i)*8);
  double * ret = ((double * )(matrix -> data)) + (j + matrix -> dims[1] * i);
  return (ret);
}
/* return a pointer to a double stored inside the Array’s data allocation */

unsigned char * getuchar(Array * arr, unsigned int i, unsigned int j) {
  //must be 2d array and have a type of unsigned integers
  if (arr -> dimno != 2 || arr -> type != UCHAR_TYPE || arr -> elno < 1) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "getuchar – invalid array\n");
    return NULL;
  }

  //returning point in data memory block by translating dimensions to a memory address
  unsigned char * ret = ((unsigned char * ) arr -> data) + (j + arr -> dims[1] * i);
  return (ret);
}
/* return a pointer to an unsigned char stored inside the Array’s data allocation */

Array * matrixcross(Array * multiplier, Array * multiplicand) {
  //multiplier is not matrix
  if (!ismatrix(multiplier)) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixcross - multiplier is not a matrix\n");
    return NULL;
  }
  //multiplicand is not matrix
  if (!ismatrix(multiplicand)) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixcross - multiplicand is not a matrix\n");
    return NULL;
  }
  //columns in multiplier does not match number of rows in multiplicand
  if (multiplier -> dims[1] != multiplicand -> dims[0]) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixcross - column row mismatch");
    return NULL;
  }

  //new array of size multiplier rows (as arr rows) * multiplicand columns (as arr columns)
  Array * arr = newarray(multiplier -> dims[0] * multiplicand -> dims[1], multiplier -> type);

  //inflating so number of columns is equal to number of columns in multiplicand
  inflatearray(arr, multiplier -> dims[0]);

  for (int i = 0; i < multiplier -> dims[0]; i++) {
    for (int j = 0; j < multiplicand -> dims[1]; j++) {
      double sum = 0.0;
      for (int k = 0; k < multiplier -> dims[1]; k++) {
        double * a = matrixgetdouble(multiplier, i, k);
        double * b = matrixgetdouble(multiplicand, k, j);
        sum += * a * * b;
      }
      // store the sum of the matrix in the result variable
      *((double * ) arr -> data + i * multiplicand -> dims[1] + j) = sum;
    }
  }

  /*
    //iterating through data and setting cross product to memory
    for(int i = 0; i < multiplier->dims[0]; i++){
      for(int j = 0; j < multiplicand->dims[1]; j++){
          double sum = 0.0;
          for (int k = 0; k < multiplier->dims[1]; k++) {
            sum += *matrixgetdouble(multiplier,i,k) * *matrixgetdouble(multiplicand,k,j);
          }
          *matrixgetdouble(arr,i,j) = sum;
      }
    }*/
  return arr;
}
/* compute a matrix-matrix multiplication of the multiplier and 
the multiplicand and return a newarray representing the product */

/* Elementwise Matric Operations */
double mulop(double x, double y) {
  return x * y;
}
/* return the product of x and y */

double addop(double x, double y) {
  return x + y;
}
/* return the sum of x and y */

double subop(double x, double y) {
  return x - y;
}
/* return the difference between x and y */

Array * matrixmatrixop(Array * arr1, Array * arr2, double( * fn)(double, double)) {
  //arr1 is not matrix
  if (!ismatrix(arr1)) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixmatrixop - arr1 is not a matrix\n");
    return NULL;
  }

  //arr2 is not matrix
  if (!ismatrix(arr2)) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixmatrixop - arr2 is not a matrix\n");
    return NULL;
  }

  //matricies must have identical dimensions
  if (arr1 -> dims[0] != arr2 -> dims[0] || arr1 -> dims[1] != arr2 -> dims[1]) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixmatrixop - bad dimensions\n");
    return NULL;
  }

  //creating deep copy of arr1
  Array * arrnew = newarray(arr1 -> dims[0] * arr1 -> dims[1], DOUBLE_TYPE);
  inflatearray(arrnew, arr1 -> dims[0]);
  //iterating through matrix and setting arrnew value to result of fn on arr1 and arr2
  for (int i = 0; i < arr1 -> dims[0]; i++) {
    for (int j = 0; j < arr1 -> dims[1]; j++) {
      double * arr1val = matrixgetdouble(arr1, i, j);
      double * arr2val = matrixgetdouble(arr2, i, j);
      double * res = matrixgetdouble(arrnew, i, j);
      * res = fn( * arr1val, * arr2val);
    }
  }

  return arrnew;
}
/* return a pointer to a newarray with dimensions matching arr1 and arr2.
Each element, i,j, in the returned array will be equal to the result of applying the function
pointed to by fn, to the corresponding elements i,j in arr1 and arr2 */

Array * matrixvectorop(Array * arr, Array * vec, double( * fn)(double, double)) {
  //arr1 is not matrix
  if (!ismatrix(arr)) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixvectorop - arr is not a matrix\n");
    return NULL;
  }

  //arr2 is not matrix
  if (!isvector(vec)) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixvectorop - vec is not a vector\n");
    return NULL;
  }

  //matrix and vector must have must have identical dimensions
  if (arr -> dimno != vec -> dimno) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixvectorop - bad dimensions\n");
    return NULL;
  }

  //creating deep copy of arr
  Array * arrnew = newarray(arr -> elno, DOUBLE_TYPE);
  inflatearray(arrnew, arr -> dims[0]);

  //iterating through matrix and setting arrnew value to result of fn on arr and vec
  for (int i = 0; i < arr -> dims[0]; i++) {
    for (int j = 0; j < vec -> dims[1]; j++) {
      double * arrval = matrixgetdouble(arr, i, j);
      double * vecval = matrixgetdouble(vec, 0, j);
      double * res = matrixgetdouble(arrnew, i, j);
      * res = fn( * arrval, * vecval);
      * matrixgetdouble(arrnew, i, j) = fn( * matrixgetdouble(arr, i, j), * matrixgetdouble(vec, 0, j));
    }
  }
  return arrnew;

}
/* operate like the matrixmatrixop except that that second matrix is a vector */

Array * scalarmatrixop(double scalar, Array * arr, double( * fn)(double, double)) {
  //arr is not matrix
  if (!ismatrix(arr)) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "scalarmatrixop - arr is not a matrix\n");
    return NULL;
  }

  //creating deep copy of arr
  Array * arrnew = newarray(arr -> elno, DOUBLE_TYPE);
  inflatearray(arrnew, arr -> dims[0]);

  //iterating through matrix and setting arrnew value to result of fn on arr and vec
  for (int i = 0; i < arr -> dims[0]; i++) {
    for (int j = 0; j < arr -> dims[1]; j++) {
      double * in = matrixgetdouble(arr, i, j);
      double * res = matrixgetdouble(arrnew, i, j);
      * res = fn(scalar, * in);
    }
  }
  return arrnew;
}
/* create a newarray of the same dimensions as arr, with element values
computed by applying the given function to the scalar as the first argument and each element
of the array as the second argument */

Array * matrixtranspose(Array * original) {
  //original is not matrix
  if (!ismatrix(original)) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixtranspose - arr is not a matrix\n");
    return NULL;
  }

  //creating new array
  Array * arrT = newarray(original -> elno, DOUBLE_TYPE);
  inflatearray(arrT, original -> dims[1]);

  //iterating through matrix and transposing original to arrT
  for (int i = 0; i < original -> dims[0]; i++) {
    for (int j = 0; j < original -> dims[1]; j++) {
      double * cis = matrixgetdouble(original, i, j);
      double * trans = matrixgetdouble(arrT, j, i);
      * trans = * cis;
    }
  }
  return arrT;
}
/* create a newarray that is the transpose of the original array */

double matrixsum(Array * arr) {
  double matrixsum = 0;

  //arr is not matrix
  if (!ismatrix(arr)) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixsum - arr is not a matrix\n");
    return 0;
  }

  //iterating through matrix and summing values
  for (int i = 0; i < arr -> dims[0]; i++) {
    for (int j = 0; j < arr -> dims[1]; j++) {
      double * num = matrixgetdouble(arr, i, j);
      matrixsum += * num;
    }
  }
  return matrixsum;
}
/* return a double value equal to the sum of all elements in arr */

Array * matrixonehot(Array * arr) {
  //arr is not matrix
  if (arr -> dimno != 1) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixonehot - bad dimensions\n");
    return NULL;
  }

  if (arr -> type != UCHAR_TYPE) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixonehot - bad type\n");
    return NULL;
  }

  //creating new array
  Array * arrnew = newarray(arr -> dims[0] * 10, DOUBLE_TYPE);

  //making array arr->elno by 10 in size
  inflatearray(arrnew, arr -> dims[0]);

  // Initialize all elements to 0.0
  for (int i = 0; i < arr -> dims[0]; i++) {
    for (int j = 0; j < 10; j++) {
      *((double * ) arrnew -> data + i * 10 + j) = 0;
    }
  }

  unsigned char * data = arr -> data;
  for (int i = 0; i < arr -> elno; i++) {
    unsigned char temp = data[i];
    *((double * ) arrnew -> data + i * 10 + temp) = 1;
  }
  return arrnew;
}
/* create a matrix of one-hot vectors based on a 1-dimensional array of
UCHAR_TYPE */

Array * matrixsumcols(Array * arr) {
  //arr is not matrix
  if (!ismatrix(arr)) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixsumcols - arr is not a matrix\n");
    return NULL;
  }

  //creating new array with size of arr's dimensions and type of int
  Array * arrnew = newarray(arr -> dims[1], DOUBLE_TYPE);

  //transposing array so it is 1xarr->dims[1]
  inflatearray(arrnew, 1);

  double * resultData = (double * ) arrnew -> data;
  for (int i = 0; i < arrnew -> dims[1]; i++) {
    resultData[i] = 0.0;
  }

  for (int col = 0; col < arr -> dims[1]; col++) {
    double temp = 0.0;
    for (int row = 0; row < arr -> dims[0]; row++) {
      double * element = matrixgetdouble(arr, row, col);
      temp += * element;
    }
    // put the  sum in the new array
    resultData[col] = temp;
  }

  return arrnew;
}
/* create a newarray that is a matrix with only one row (index 0). The values
in each column of the new array should equal the sum down the corresponding column of the
original array */

Array * arrgetmatrix(Array * arr, unsigned int i) {
  //verifying 3-d array
  if (arr -> dimno != 3) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "arrgetmatrix - arr is not a 3-d array\n");
    return NULL;
  }

  //new array of size j and k from arr
  Array * arrnew = newarray(arr -> dims[1] * arr -> dims[2], arr -> type);

  //making array x by y in size and dimensions
  inflatearray(arrnew, arr -> dims[1]);

  //iterating through matrix and setting new array values to proper arr 'frame'
  for (int j = 0; j < arr -> dims[1]; j++) {
    for (int k = 0; k < arr -> dims[2]; k++) {
      arrnew -> data[j * arr -> dims[2] + k] = arr -> data[i * arr -> dims[1] * arr -> dims[2] + j * arr -> dims[2] + k];
    }
  }
  return arrnew;

}
/* create a new matrix that is from a array of different matrices. 
The matrix to be selected is specified by i.
*/

Array * matrixtodouble(Array * arr) {

  //verifying 2-d array
  if (arr -> dimno != 2) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixtodouble - arr is not a 2-d array\n");
    return NULL;
  }

  //verifying type
  if (arr -> type != UCHAR_TYPE) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixtodouble – not type UCHAR\n");
    return NULL;
  }
  //new array of size i and j from arr
  Array * arrnew = newarray(arr -> elno, DOUBLE_TYPE);

  inflatearray(arrnew, arr -> dims[0]);

  for (int i = 0; i < arr -> dims[0]; i++) {
    for (int j = 0; j < arr -> dims[1]; j++) {
      unsigned char * charval = getuchar(arr, i, j);
      double * doubval = matrixgetdouble(arrnew, i, j);
      * doubval = (double)( * charval);

    }
  }
  return arrnew;
}

Array * matrixonecold(Array * arr) {
  //arr is not matrix
  if (arr -> dimno != 2) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixonecold - bad dimensions\n");
    return NULL;
  }

  if (arr -> type != DOUBLE_TYPE) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixonecold - bad type\n");
    return NULL;
  }

  //creating new array size dims[0], number of rows in arr
  Array * arrnew = newarray(arr -> dims[0], UCHAR_TYPE);

  double temp_grand = 0.0;
  int index = 0;

  //iterating through array and setting arrnew based on largest value within arr rows
  for (int i = 0; i < arr -> dims[0]; i++) {
    temp_grand = * matrixgetdouble(arr, i, 0);
    index = 0;
    for (int j = 1; j < arr -> dims[1]; j++) {
      if ( * matrixgetdouble(arr, i, j) > temp_grand) {
        temp_grand = * matrixgetdouble(arr, i, j);
        index = j;
      }
    }
    *((unsigned char * ) arrnew -> data + i) = index;
    //*(unsigned char*)(arrnew->data + (ELEMENT_SIZE(arr->type)*i)) = temp_grand;
  }
  return arrnew;
}
/* return 1 dimesnional array with each row containing the value of the index 
of the column of the corresponding input array with the highest value across the row
*/

Array * matrixconfusion(Array * val, Array * tar) {
  //val and tar are 1d and of same size
  if (val -> dimno != 1 || tar -> dimno != 1 || tar -> elno != val -> elno) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixconfusion - bad dimensions\n");
    return NULL;
  }

  // val and tar are uchar type
  if (val -> type != UCHAR_TYPE || tar -> type != UCHAR_TYPE) {
    ERROR_CODE = ERR_VALUE;
    strcpy(ERROR_STRING, "matrixconfusion - bad type\n");
    return NULL;
  }

  //new array of size 10x10
  Array * arrnew = newarray(10 * 10, DOUBLE_TYPE);

  //making array 10x10 in size and dimensions
  inflatearray(arrnew, 10);

  int temp_counter = 0;

  //iterating through matrix setting arrnew i,j to confusion result
  for (int i = 0; i < arrnew -> dims[0]; i++) {
    for (int j = 0; j < arrnew -> dims[1]; j++) {
      temp_counter = 0;
      //val and tar confusion loop
      for (int k = 0; k < val -> dims[0]; k++) {
        if ( * ((unsigned char * )(val -> data + (ELEMENT_SIZE(val -> type) * k))) == i &&
          *
          ((unsigned char * )(val -> data + (ELEMENT_SIZE(val -> type) * k))) == j) {
          temp_counter++;
        }
      }
      * matrixgetdouble(arrnew, i, j) = temp_counter;
    }
  }

  return arrnew;
}
/* returns 10x10 array where i,j are the number of times the val array contains i,
and the number of times the tar array contains j in the same row
*/
