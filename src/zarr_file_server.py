from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import PurePath
import threading
import platform
import os
from subprocess import Popen, DEVNULL

import pkg_resources

# Thread local variable with .dir parameter specifying what dir the server should be on
local = threading.local()

class CORSRequestHandler (SimpleHTTPRequestHandler):
    """
    Handler which adds CORS functionality to python's built in http.server
    and uses directory referenced by local.dir

    Args:
        SimpleHTTPRequestHandler (_type_): http.server handler to extend functionality on
    """
    def __init__(self, *args, **kwargs):

        SimpleHTTPRequestHandler.protocol_version = "HTTP/1.1"
        super().__init__(directory=local.dir, *args, **kwargs)

    def do_GET(self) -> None:
        self.send_response(206, "Partial Content")
        return super().do_GET()

    def end_headers (self):
        """
        Sends CORS line ending the MIME headers
        """
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Connection", "keep-alive")
        self.send_header("Accept-Ranges", "*")
        self.send_header("keep-alive", "timeout=5")
        self.send_header("access-control-allow-headers", "*")
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        """
        Handles OPTION requests as SimpleHTTPRequestHandler is unable to by default
        """
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
    
#    def log_message(self, format, *args):
        """
        NOTE - Overrides HTTPServer.log_message()

        Omit output such that jupyter notebooks won't be covered in request info

        Args:
            format (_type_): _description_
        """
#        pass

def host_file(path:PurePath, port:int=0)->None:
    """
    Generates a web server which points to a file directory.

    NOTE - runs forever, call in a separate thread to run concurrently.
    Args:
        path (Purepath): File path pointing to a .zarr file
        port (int): port number to plug server into (default is 0 which is 1st available socket found)
    """

    #with HTTPServer(("", port), CORSRequestHandler) as httpd:
        # Set dir
       
    pointer = None
    if os.path.isdir(path):
        local.dir = path
    else:
        local.dir = os.path.dirname(path)

    os_name = platform.system()
    if os_name == "Windows":
        Popen([pkg_resources.resource_filename(__name__, "apps/http-server/http-server-win.exe"), "--port", f"{port}", local.dir, "--cors", "-s"], stderr=DEVNULL, stdout=DEVNULL)
    elif os_name == "Darwin":
        Popen([pkg_resources.resource_filename(__name__, "apps/http-server/http-server-macos"), "--port", f"{port}", local.dir, "--cors", "-s"], stderr=DEVNULL, stdout=DEVNULL)
    else:
        Popen([pkg_resources.resource_filename(__name__, "apps/http-server/http-server-linux"), "--port", f"{port}", local.dir, "--cors", "-s"], stderr=DEVNULL, stdout=DEVNULL)

    # Serve files
    #httpd.serve_forever()