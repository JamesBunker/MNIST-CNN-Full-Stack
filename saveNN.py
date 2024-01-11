import mxarrsql;
import mxarr;
import sys;

if len(sys.argv)!=4:
    print( "usage:  %s name epoch minibatch\n" % sys.argv[0] );
    sys.exit(1);

basename = sys.argv[1]+'['+sys.argv[2]+','+sys.argv[3]+']';

print( 'basename = ', repr(basename) );
#sck_mnist[8,0].i2h
db = mxarrsql.Database();

for extension in [ '.i2h', '.b2h', '.h2o', '.b2o' ]:
    fullname = basename + extension;

    print( "loading: ", fullname );
    arr = db.retrieve_arr( basename + extension );

    filename = sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+extension;

    print( "saving:", filename );
    fp = mxarr.fopen( filename, "wb" );
    mxarr.writearray( fp, 0, arr );
    mxarr.fclose( fp );


db.close();
