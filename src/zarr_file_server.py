from http.server import HTTPServer, SimpleHTTPRequestHandler
from os import chdir
from pathlib import PurePath
import threading

local = threading.local()
class CORSRequestHandler (SimpleHTTPRequestHandler):
    """
    Handler which adds CORS functionality to python's built in http.server

    Args:
        SimpleHTTPRequestHandler (_type_): http.server handler to extend functionality on
    """
    def __init__(self, *args, **kwargs):
        #print(local.dir)
        super().__init__(directory=local.dir, *args, **kwargs)

    def end_headers (self):
        """
        Sends CORS line ending the MIME headers
        """
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        """
        Handles OPTION requests as SimpleHTTPRequestHandler is unable to by default
        """
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
    
    def log_message(self, format, *args):
        """
        NOTE - Overrides HTTPServer.log_message()

        Omit output such that jupyter notebooks won't be covered in request info

        Args:
            format (_type_): _description_
        """
        pass
def host_zarr(zarr_file_path:PurePath, port:int=0)->None:
    """
    Generates a web server which points to a .zarr file.

    NOTE - runs forever, call in a separate thread to run concurrently.
    Args:
        zarr_file_path (Purepath): File path pointing to a .zarr file
        port (int): port number to plug server into (default is 0 which is 1st available socket found)
    """

    with HTTPServer(("", port), CORSRequestHandler) as httpd:
        global dir
        local.dir = zarr_file_path
        httpd.serve_forever()