from IPython.display import display, IFrame
from urllib.parse import ParseResult
from pathlib import PurePath
from zarr_file_server import host_zarr
from threading import Thread
from socket import socket

def get_free_port()->int:
    """
    Grabs any free port available on the system

    Return: A free port on the system
    """

    sock = socket()  # Creates a socket
    sock.bind(('', 0))      
    port = sock.getsockname()[1]
    sock.close()
    return port

def render(path:ParseResult|PurePath = "", width:int=960, height:int=500, port:int=0)->None:
    """
    Displays "https://render.ci.ncats.io/" with args to specify display dimensions, port to serve
    .zarr files to Polus Render, and dataset to use.
    
    Param:
        path (ParseResult|Purepath): Acquired from urllib.parse.ParseResult or Path, renders url in render.
                            If not specified, renders default render url
        width (int): width of render to be displayed, default is 960
        height (int): height of render to be displayed, default is 500
        port (int): Port to run local zarr server on if used (default is 0 which is the 1st available port).
    Pre: port selected (if used) is not in use IF path given is Purepath
        
    """

    # Extract url from local file path if provided. ?imageUrl is required scheme for render
    if isinstance(path, PurePath):
        # We could've call 0 in host_zarr to use a random server but we need to know the port number to display render
        if port == 0:
            port = get_free_port()
        # NOTE - uses local http server to serve local file to render, ran multithreaded b/c server does not end
        Thread(target=host_zarr, args=(path,port,)).start()
        path = "?imageUrl=http://localhost:" + str(port) + "/"

    # Otherwise, extract url from user provided url if provided
    elif isinstance(path, ParseResult):
        path = "?imageUrl=" + path.geturl() # Can be manually rebuilt to check if a valid format url is sent
    
    print(f"rendering https://render.ci.ncats.io/{path}")
    # Display render
    display(IFrame(src=("https://render.ci.ncats.io/" + path)
                                                        , width=width, height=height))
    