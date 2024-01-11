import sys  # used to get argv
import cgi  # used to parse Mutlipart FormData
# this should be replace with multipart in the future

# import mxarr
import ArrDisplay
#export LD_LIBRARY_PATH=/home/undergrad/2/bunkerj/CIS2750/A0/
#export LD_LIBRARY_PATH=C:\Users\Colvin\Desktop\Guelph\CIS_2750\A4\
#export LD_LIBRARY_PATH=C:/Users/Colvin/Desktop/Guelph/CIS_2750/A4/


import createdb
import listarr
import mxarrsql
import os
import datetime
import conf
import mxarr

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl, urlunparse


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

db = mxarrsql.Database()

# HTML strings for relevant server functionality, dynamically edited later
start_page_html = """<HTML>
  <HEADER>
    <TITLE> MNIST Machine Learning - Handwritten Images to Text </TITLE>
  </HEADER>
  <BODY>
    <h4> Create Tables </h4>
    <a href="createtables.html" target="_self">
      <button> Submit </button>
    </a>

    <h4> List Arrays </h4>
    <a href="listarrays.html" target="_self">
      <button> Submit </button>
    </a>

    <h4> Run NN in Background </h4>
    <FORM action="launchNN.html" method="post" enctype="multipart/form-data">
    <label for="name">Name:</label><br>
    <input type="text" id="name" name="name" value="" required><br>
    <label for="start">Start Epoch:</label><br>
    <input type="text" id="start" name="start" value="" required><br>
    <label for="end">End Epoch:</label><br>
    <input type="text" id="end" name="end" value="" required><br><br>
    <input type="submit" value="Submit">
    </form> 

    <h4> *.l2 Files </h4>
    <a href="displayl2.html" target="_self">
      <button> Submit </button>
    </a>

    <h4>  NN Verification and Viewer </h4>
    <a href="load_NN.html" target="_self">
      <button> Submit </button>
    </a>

    <P>Hit the "Submit" button to go to the corresponding page.
    </P>
  </BODY>
</HTML>
"""

create_table_html = """<HTML>
  <HEADER>
    <TITLE> MNIST Machine Learning - Handwritten Images to Text </TITLE>
  </HEADER>
  <BODY>
    <a href="startpage.html" target="_self">
      <button> Home </button>
    </a>

    <P>Tables have sucessfully be created, click the button to return home.</P>
  </BODY>
</HTML>
"""

list_array_html = """<HTML>
  <HEADER>
    <TITLE> MNIST Machine Learning - Handwritten Images to Text </TITLE>
  </HEADER>
  <BODY>
    <a href="startpage.html" target="_self">
      <button> Home </button>
    </a>

    <FORM action="deletearrays.html" method="post" enctype="multipart/form-data">
    <INPUT type="Submit" id="Create" name="Create" /><br/>
"""

run_NN_html = """<HTML>
  <HEADER>
    <TITLE> MNIST Machine Learning - Handwritten Images to Text </TITLE>
  </HEADER>
  <BODY>
    <a href="startpage.html" target="_self">
      <button> Home </button>
    </a>

    <P>Neural Network running in background, click the button to return home.</P>
  </BODY>
</HTML>
"""

l2_list_html = """<HTML>
  <HEADER>
    <TITLE> MNIST Machine Learning - Handwritten Images to Text </TITLE>
  </HEADER>
  <BODY>
    <a href="startpage.html" target="_self">
      <button> Home </button>
    </a>
"""

l2_graph_html = """<HTML>
  <HEADER>
    <TITLE> MNIST Machine Learning - Handwritten Images to Text </TITLE>
  </HEADER>
  <BODY>
    <a href="startpage.html" target="_self">
      <button> Home </button>
    </a>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script> 
        function inf(){
          $(document).ready(function(){
              $.get("%s.html", function(data){
              $("#svg_box").load("graph.svg");
              });
          });
          setTimeout(inf,1000);

        };
        inf();
</script>

  <div id="svg_box">
  </div>

    <P>Live error of neural network, click the button to return home.</P>
  </BODY>
</HTML>
"""

load_NN_html = """<HTML>
  <HEADER>
    <TITLE> MNIST Machine Learning - Handwritten Images to Text </TITLE>
  </HEADER>
  <BODY>
    <a href="startpage.html" target="_self">
      <button> Home </button>
    </a>
"""

view_html_file = """<HTML>
  <HEADER>
    <TITLE> Image Viewer </TITLE>
  </HEADER>
  <BODY>
    <a href="startpage.html" target="_self">
      <button> Home </button>
    </a>

    <a href="view%s_{0}.html" target="_self">
      <button> Prev </button>
    </a>

    <a href="view%s_{0}.html" target="_self">
      <button> Next </button>
    </a>

    <LABEL for="photo">True Label:{1}</LABEL><br/>
    <IMG src= "img%s.svg" />

    <P>Hit the "Next" or "Prev" button, to send the form as a GET request to the server.
    </P>
  </BODY>
</HTML>
"""

# handler for our web-server - handles both GET and POST requests
class MyHandler(BaseHTTPRequestHandler):
    data_path = ""
    def do_GET(self):
        # parse the URL to get the path and form data
        parsed = urlparse(self.path)

        # check if the web-pages matches the list
        if parsed.path in ['/startpage.html']:
            # get the form data and turn it into a dictionary
            form_data = dict(parse_qsl(parsed.query))

            # dynamically create html file
            content = start_page_html % form_data

            # generate the headers
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            # send it to the browser
            self.wfile.write(bytes(content, "utf-8"))

        elif "/createtables" in parsed.path:
            # dynamically create html file
            content = create_table_html

            createdb

            self.send_response(200)  # OK
            # notice the change in Content-type
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))  # binary file

        elif "/listarrays" in parsed.path:
            list_array_footer ="""    </FORM>
                <P>Select arrays and click the submit button to delete them, click the home button to return home.</P>
                </BODY>
                </HTML>
                """
            list_array_html_segment = """
                <input type="checkbox" id="{0}" name="{0}" value="{0}">
                <label for="{0}"> {0}</label><br>
                """
            # dynamically create html file
            content = list_array_html

            array_list = db.listarr()

            for arr in array_list:
                content += list_array_html_segment.format(arr)
            
            content += list_array_footer

            self.send_response(200)  # OK
            # notice the change in Content-type
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))  # binary file

        elif "/displayl2" in parsed.path:

            l2_list_footer ="""
                <P>Click link to view l2 error live, click the home button to return home.</P>
                </BODY>
                </HTML>
                """
            l2_list_segment = """
                <p><a href="{0}.html">{1}</a></p>
                """
            # dynamically create html file
            content = l2_list_html
            file_mod_list = []

            for root, dirs, files in os.walk(os.getcwd()):
                for file in files:
                    if file.endswith('.l2'):
                        file_mod_list.append([file, str(modification_date(file))])
            file_mod_list.sort(key=lambda x:x[1],reverse=True)

            for f in file_mod_list:
                content += l2_list_segment.format(f[0], f[0] + "\t-----\tLast Modified: " + f[1])

            content += l2_list_footer

            self.send_response(200)  # OK
            # notice the change in Content-type
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))  # binary file

        #may need vaguer name
        elif ".l2" in parsed.path:
            data_path = self.path.removesuffix(".html").removeprefix("/")

            #graph_values = ArrDisplay.load_arr(data_path)
            #print(graph_values.getdim(0))
            #graph = ArrDisplay.graph(graph_values, ["0", "90", "180", "270", "360" ],["-1.0","-0.5","0.0","0.5","1.0"],0, 1,600/360, 400/2 )

            f = open("param.inf", "w")
            f.write(data_path)
            f.close()

            # dynamically create html file
            content = l2_graph_html % data_path

            self.send_response(200)  # OK
            # notice the change in Content-type
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))  # binary file
        elif "/graph.svg" in parsed.path:
            with open('param.inf') as f:
              path = f.readline()
            f.close()

            lins = sum(1 for _ in open(path))
            content = ArrDisplay.lazygraph(path, ["Epoch Progress"],["0","20","40","60","80"],0, 1, 600/lins, 400/80)

            # dynamically create html file
            # generate the headers
            self.send_response(200)  # OK
            self.send_header("Content-type", "image/svg+xml")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))  # binary file
        
        elif "/load_NN" in parsed.path:
            
            list_array_footer ="""    </FORM>
                <P>Select NN and click the submit button to go to image viewing and NN testing click the home button to return home.</P>
                </BODY>
                </HTML>
                """
            l2_list_segment = """
                <p><a href="view0000_{0}.html">{0}</a></p>
                """

            # dynamically create html file
            content = load_NN_html

            array_list = db.listarr()
            for arr in array_list:
                arr = arr.split(".")[0]

            array_list = list(dict.fromkeys(array_list))

            for arr in array_list:
                content += l2_list_segment.format(arr)
              
            content += list_array_footer

            self.send_response(200)  # OK
            # notice the change in Content-type
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))  # binary file
        
        elif "/view" in parsed.path:
            path = self.path.split("_")[-1].removesuffix(".html")

            # getting the current page number from the URL
            current_page = int(''.join(x for x in self.path.split("_")[0] if x.isdigit()))

            # logic for rolling over next and previous functionality
            if current_page == 9999:
                next_page = 0
            else:
                next_page = current_page + 1
            if current_page == 0:
                prev_page = 9999
            else:
                prev_page = current_page - 1

            fp = mxarr.fopen( "t10k-labels-idx1-ubyte", "rb" )
            data = mxarr.readarray( fp )
            mxarr.fclose( fp )
            data.inflate(data.getdim(0))

            true_label = int(data[current_page,0])

            file = view_html_file.format(path,true_label)

            #need conf: test label, actual label, confunsion matrix from path NN output


            # dynamically create html file
            content = (file % (
            format(prev_page, '04d'), format(next_page, '04d'), format(current_page, '04d')))

            self.send_response(200)  # OK
            # notice the change in Content-type
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))  # binary file

        elif "/img" in parsed.path:
            # getting the current page number from the URL
            current_page = int(''.join(x for x in self.path if x.isdigit()))



            # get array data from uploaded file in upload
            data = ArrDisplay.get_arr("t10k-images-idx3-ubyte", current_page)
            content = ArrDisplay.svg(data)

            self.send_response(200)  # OK
            # notice the change in Content-type
            self.send_header("Content-type", "image/svg+xml")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))  # binary file
        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))

    def do_POST(self):
        # hanle post request
        # parse the URL to get the path and form data
        parsed = urlparse(self.path)
  
        if parsed.path in ['/deletearrays.html']:
            delete_arrays_html = """<HTML>
                <HEADER>
                    <TITLE> MNIST Machine Learning - Handwritten Images to Text </TITLE>
                </HEADER>
                <BODY>
                    <a href="listarrays.html" target="_self">
                    <button> Return </button>
                    </a>

                    <P>Selected arrays have been deleted, click the button to return to array selection.</P>
                </BODY>
                </HTML>
                """

            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage(fp=self.rfile,
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                             'CONTENT_TYPE':
                                                 self.headers['Content-Type'],
                                             }
                                    )

            array_list = db.listarr()

            for arr in array_list:
                if form.getvalue(arr):
                    db.deletearr(arr)

            content = delete_arrays_html

            # generate the headers
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            # send it to the browser
            self.wfile.write(bytes(content, "utf-8"))
        elif parsed.path in ['/launchNN.html']:

            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage(fp=self.rfile,
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                             'CONTENT_TYPE':
                                                 self.headers['Content-Type'],
                                             }
                                    )
            content = run_NN_html % form
            
            os.system( "python3 NN.py " + form.getvalue('name') + " " + form.getvalue('start') + " " + form.getvalue('end') + " &")

            # generate the headers
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            # send it to the browser
            self.wfile.write(bytes(content, "utf-8"))

        elif parsed.path in ['/viewer.html']:

            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage(fp=self.rfile,
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                             'CONTENT_TYPE':
                                                 self.headers['Content-Type'],
                                             }
                                    )
            content = run_NN_html % form
            
            os.system( "python3 NN.py " + form.getvalue('name') + " " + form.getvalue('start') + " " + form.getvalue('end') + " &")

            # generate the headers
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            # send it to the browser
            self.wfile.write(bytes(content, "utf-8"))
        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))

httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
print("Server listing in port:  ", int(sys.argv[1]))
httpd.serve_forever()
