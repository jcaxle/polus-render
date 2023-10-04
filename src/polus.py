from IPython.display import display, IFrame
from urllib.parse import ParseResult
from pathlib import PurePath
from zarr_file_server import host_file
from threading import Thread
from socket import socket

RENDER_URL = "http://localhost:4200/"

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

def render(image_location:ParseResult|PurePath = "", microjson_overlay_location:ParseResult|PurePath = "", width:int=960, height:int=500, image_port:int=0, microjson_overlay_port:int=0)->None:
    """
    Displays "https://render.ci.ncats.io/" with args to specify display dimensions, port to serve,
    image files to use, and overlay to use.
    
    Param:
        image_location(ParseResult|Purepath): Acquired from urllib.parse.ParseResult or Path, renders url in render.
                            If not specified, renders default render url.
        microjson_overlay_location(ParseResult|Purepath): Acquired from urllib.parse.ParseResult or Path, renders url in render.
                            If not specified, renders default render url
        width (int): width of render to be displayed, default is 960
        height (int): height of render to be displayed, default is 500
        image_port (int): Port to run local zarr server on if used (default is 0 which is the 1st available port).
        microjson_overlay_port (int): Port to run local json server on if used (default is 0 which is the 1st available port).
    Pre: zarr_port and json_port selected (if used) is not in use IF path given is Purepath
        
    """

    # Extract url from local file path if provided. ?imageUrl is required scheme for render
    if isinstance(image_location, PurePath):
        # We could've call 0 in host_file to use a random server but we need to know the port number to display render
        if image_port == 0:
            image_port = get_free_port()
        # NOTE - uses local http server to serve local file to render, ran multithreaded b/c server does not end
        Thread(target=host_file, args=(image_location,image_port,)).start()
        image_location = "?imageUrl=http://localhost:" + str(image_port) + "/"

    # Otherwise, extract url from user provided url if provided
    elif isinstance(image_location, ParseResult):
        image_location = "?imageUrl=" + image_location.geturl() # Can be manually rebuilt to check if a valid format url is sent
    
    # Do the same but for JSON
    if isinstance(microjson_overlay_location, PurePath):
        if microjson_overlay_port == 0:
            microjson_overlay_port = get_free_port()
        Thread(target=host_file, args=(microjson_overlay_location,microjson_overlay_port,)).start()
        microjson_overlay_location = "&overlayUrl=http://localhost:" + str(microjson_overlay_port) + f"/{(microjson_overlay_location.name)}" 

    elif isinstance(microjson_overlay_location, ParseResult):
        microjson_overlay_location = "&overlayUrl=" + microjson_overlay_location.geturl()    


    print(f"rendering {RENDER_URL}{image_location}{microjson_overlay_location}")
    # Display render
    display(IFrame(src=(f"{RENDER_URL}{image_location}{microjson_overlay_location}")
                                                        , width=width, height=height))
    