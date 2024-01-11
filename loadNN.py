import mxarrsql;
import mxarr;
import sys;
db = mxarrsql.Database();
fp = mxarr.fopen( "sck_mnist_40_0.i2h", "rb" );
i2h = mxarr.readarray( fp );
mxarr.fclose( fp );

fp = mxarr.fopen( "sck_mnist_40_0.b2h", "rb" );
b2h = mxarr.readarray( fp );
mxarr.fclose( fp );

fp = mxarr.fopen( "sck_mnist_40_0.h2o", "rb" );
h2o = mxarr.readarray( fp );
mxarr.fclose( fp );

fp = mxarr.fopen( "sck_mnist_40_0.b2o", "rb" );
b2o = mxarr.readarray( fp );
mxarr.fclose( fp );

db.store_arr( 'prof1[40,0].i2h',  i2h  );
db.store_arr( 'prof1[40,0].b2h',  b2h  );
db.store_arr( 'prof1[40,0].h2o',  h2o  );
db.store_arr( 'prof1[40,0].b2o',  b2o  );
db.close();


