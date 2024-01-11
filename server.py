import sys  # used to get argv
import cgi  # used to parse Mutlipart FormData
# this should be replace with multipart in the future

# import mxarr
import ArrDisplay
#export LD_LIBRARY_PATH=/home/undergrad/2/bunkerj/CIS2750/A0/

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl, urlunparse

# HTML strings for relevant server functionality, dynamically edited later
upload_html_file = """<HTML>
  <HEADER>
    <TITLE> Upload </TITLE>
  </HEADER>
  <BODY>
    <h2> Uploading File to Server</h2>
    <FORM action="uploaded.html" method="post" enctype="multipart/form-data">
    <LABEL for="svgfile">Upload t10k-images-idx-ubyte:</LABEL><br/>
    <INPUT type="file" id="svgfile" name="svgfile" /><br/>
    <INPUT type="Submit" id="Submit" name="Submit" /><br/>
    </FORM>
    <P>Hit the "Submit" button, to send the form as a POST request to the server
    with path "uploaded.html".
    </P>
  </BODY>
</HTML>
"""

uploaded_html_file = """<HTML>
  <HEADER>
    <TITLE> Upload </TITLE>
  </HEADER>
  <BODY>
    <h2> Uploading File to Server</h2>
    <LABEL for="svgfile">File:</LABEL><br/>
    %(svgfile)s<br><br/>
    <P>File uploaded to working directory.
    </P>
  </BODY>
</HTML>
"""

view_html_file = """<HTML>
  <HEADER>
    <TITLE> Image Viewer </TITLE>
  </HEADER>
  <BODY>
  
    <a href="view%s.html" target="_self">
      <button> Next </button>
    </a>

    <a href="view%s.html" target="_self">
      <button> Prev </button>
    </a>

    <LABEL for="photo">Photo:</LABEL><br/>
    <IMG src= "img%s.svg" />

    <P>Hit the "Next" or "Prev" button, to send the form as a GET request to the server.
    </P>
  </BODY>
</HTML>
"""

upload2_html_file = """<HTML>
  <HEADER>
    <TITLE> Upload2 </TITLE>
  </HEADER>
  <BODY>
    <h2> Graph Function with Uploaded File </h2>
    <FORM action="graph.svg" method="post" enctype="multipart/form-data">
    <LABEL for="file">Upload Graph Compatible File:</LABEL><br/>
    <INPUT type="file" id="graphfile" name="graphfile" /><br/>
    <INPUT type="Submit" id="Submit" name="Submit" /><br/>
    </FORM>

    <P>Hit the "Submit" button, to send the form as a POST request to the server
    with path "graph.svg".
    </P>
  </BODY>
</HTML>
"""

upload2_html_file = """<HTML>
  <HEADER>
    <TITLE> Upload2 </TITLE>
  </HEADER>
  <BODY>
    <h2> Uploading File to Server</h2>
    <FORM action="graph.svg" method="post" enctype="multipart/form-data">
    <LABEL for="graphfile">Upload graph compatible file:</LABEL><br/>
    <INPUT type="file" id="graphfile" name="graphfile" /><br/>
    <INPUT type="Submit" id="Submit" name="Submit" /><br/>
    </FORM>
    <P>Hit the "Submit" button, to send the form as a POST request to the server
    with path "graph.svg".
    </P>
  </BODY>
</HTML>
"""

# handler for our web-server - handles both GET and POST requests
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # parse the URL to get the path and form data
        parsed = urlparse(self.path)

        # check if the web-pages matches the list
        if parsed.path in ['/upload.html']:
            # get the form data and turn it into a dictionary
            form_data = dict(parse_qsl(parsed.query))

            # dynamically create html file
            content = upload_html_file % form_data

            # generate the headers
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            # send it to the browser
            self.wfile.write(bytes(content, "utf-8"))

        elif "/view" in parsed.path:
            # getting the current page number from the URL
            current_page = int(''.join(x for x in self.path if x.isdigit()))

            # logic for rolling over next and previous functionality
            if current_page == 9999:
                next_page = 0
            else:
                next_page = current_page + 1
            if current_page == 0:
                prev_page = 9999
            else:
                prev_page = current_page - 1

            # dynamically create html file
            content = (view_html_file % (
            format(next_page, '04d'), format(prev_page, '04d'), format(current_page, '04d')))

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
            data = ArrDisplay.get_arr("uploaded_file.dat", current_page)
            content = ArrDisplay.svg(data)

            self.send_response(200)  # OK
            # notice the change in Content-type
            self.send_header("Content-type", "image/svg+xml")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))  # binary file

        elif '/upload2' in  parsed.path:
            # get the form data and turn it into a dictionary
            form_data = dict(parse_qsl(parsed.query))

            # dynamically create html file
            content = upload2_html_file % form_data

            # generate the headers
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            # send it to the browser
            self.wfile.write(bytes(content, "utf-8"))
        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))

    def do_POST(self):
        # hanle post request
        # parse the URL to get the path and form data
        parsed = urlparse(self.path)

        if parsed.path in ['/uploaded.html']:

            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage(fp=self.rfile,
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                             'CONTENT_TYPE':
                                                 self.headers['Content-Type'],
                                             }
                                    )
            content = uploaded_html_file % form

            # open file for binary write
            fp = open("uploaded_file.dat", 'wb')
            # read the file that came in the form and write it to local dir
            fp.write(form['svgfile'].file.read())
            fp.close()

            # generate the headers
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            # send it to the browser
            self.wfile.write(bytes(content, "utf-8"))
            fp.close()

        elif '/graph.svg' in parsed.path:
            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage(fp=self.rfile,
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                             'CONTENT_TYPE':
                                                 self.headers['Content-Type'],
                                             }
                                    )

            # open file for binary write
            fp = open("uploaded_file_graph.dat", 'wb')

            # read the file that came in the form and write it to local dir
            fp.write(form['graphfile'].file.read())
            fp.close()

            # load array from file and call graph function
            data = ArrDisplay.load_arr("uploaded_file_graph.dat")
            content = ArrDisplay.graph(data, ["0", "90", "180", "270", "360" ],["-1.0","-0.5","0.0","0.5","1.0"],0, 1,600/360, 400/2 )

            # generate the headers
            self.send_response(200)  # OK
            self.send_header("Content-type", "image/svg+xml")
            self.send_header("Content-length", len(content))
            self.end_headers()

            # send it to the browser
            self.wfile.write(content.encode())
            fp.close()

        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))

httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
print("Server listing in port:  ", int(sys.argv[1]))
httpd.serve_forever()
