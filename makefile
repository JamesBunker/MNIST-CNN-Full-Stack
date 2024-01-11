CC=clang
CFLAGS= -Wall -pedantic -std=c99

all: mxarr.o libmxarr.so swig_mxarr mxarr_wrap.o _mxarr.so batch.o libbatch.so swig_batch batch_wrap.o _batch_wrap.so

mxarr.o: mxarr.c mxarr.h
	$(CC) $(CFLAGS) -c mxarr.c -fPIC -o mxarr.o

libmxarr.so: mxarr.o
	$(CC) -shared -o libmxarr.so mxarr.o 

swig_mxarr: mxarr.i
	swig -python mxarr.i

mxarr_wrap.o: mxarr_wrap.c
	$(CC) $(CFLAGS) -c mxarr_wrap.c -fPIC -I/usr/include/python3.11 -o mxarr_wrap.o

_mxarr.so: mxarr_wrap.o
	$(CC) $(CFLAGS) -shared -dynamiclib mxarr_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lmxarr -o _mxarr.so 

batch.o: batch.c
	$(CC) $(CFLAGS) -c batch.c -o batch.o

libbatch.so: batch.o
	$(CC) -shared -o libbatch.so batch.o -L. -lmxarr -lm

swig_batch: batch.i
	swig -python batch.i

batch_wrap.o: batch_wrap.c
	$(CC) $(CFLAGS) -c batch_wrap.c -fPIC -I/usr/include/python3.11 -o batch_wrap.o

_batch_wrap.so: batch_wrap.o
	$(CC) $(CFLAGS) -shared batch_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lbatch -dynamiclib -o _batch.so 
clean: 
	-rm -f *.o *.so
