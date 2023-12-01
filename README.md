# Polus Render

`polus-render` makes Polus Render available as a Pypi package for Jupyter Lab.

Polus Render allows visualizing tiled raster datasets in Zarr and TIFF formats, as well as vector overlays in MicroJSON format. It uses lookup tables to map intensity values in these datasets to colors.

The are three ways to load the data:

1. Specifying a URL to a server serving the data.
2. Specifying a local path to a file from JupyterLab.
3. Dragging-and-dropping the dataset does not use a server.

Please note that [jupyterlab_polus_render](https://github.com/PolusAI/jupyterlab-extensions/tree/master/jupyterlab_polus_render) is the improved version of this package.

![image](https://github.com/jcaxle/polus-render/assets/145499292/2fcd525e-d97a-40fa-87f8-37981bd24be1)

# Requirements
* Python 3.9+
* [polus-server-ext](https://github.com/jcaxle/polus-server-ext) iff running jupyter notebooks remotely.

# Installation
```
pip install polus-render
```

# Dev Installation
```
git clone https://github.com/jcaxle/polus-render.git
cd polus-render
[optional] python -m venv venv
[optional] "venv/Scripts/Activate"
pip install -r requirements.txt
```
Optional steps refer to setting up venv which is recommended.

# Project File Structure
```
polus-render
| Build Instructions.md           // Instructions on how to update Pypi project
| MANIFEST.in                     // Packaging entries
| pyproject.toml                  // Pypi config 
| README                          
| requirements.txt
└───polus
    | polus_render.py                    // Main file, contains render function used by user
    | render_server.py         // Contains server only used for serving local build of Polus Render
    ├───apps           
    │   ├───render-ui              // Static Polus Render files
    │   └───updog-render           // Server used for serving files.
```

# Build Instructions
- cd to polus-render root directory.
- 'py -m build'
- 'py -m twine upload  dist/*'
- Enter '__token__' as user and reference API keys for password

# Adding a static build of Polus Render
- Remove all existing files in '~/polus-render/polus/apps/render-ui'. 
- Run 'npx nx build render-ui' in your Polus Render folder
- Tranfer generated files from '/Polus Render/dist/apps/render-ui' into '/polus-render/polus/apps/render-ui'. 

# Submodules
- [Updog-Render](https://github.com/jcaxle/updog-render/tree/71b6b938452f63412eea8edf29b9ff10f4c243dd)

# Static Render Features
| Version           | Zarr from URL/Path | TIF from URL/Path   | Micro-JSON Support | Zarr/TIF Drag & Drop | Micro-JSON Drag & Drop | 
|----------------|---------------|---------------|----------------|-----------|-----|
| Local | :heavy_check_mark:  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:

# Drag & Drop Demo
![ezgif-4-7162ca42b5](https://github.com/jcaxle/polus-render/assets/145499292/7a59db1e-3128-4ee0-b9cc-ad1be7d3faee)

# Sample usage
``` Python
from polus.polus_render import render, nb_render

# pathlib and urllib are built-ins
from urllib.parse import urlparse
from pathlib import Path

# Embeds an IFrame of a static build of Polus Render into Jupyter Notebooks
render()

# Embeds an IFrame of Polus Render into Jupyter Notebooks
render(use_local_render=False)

# Embeds an IFrame of a static build of Polus Render with an image file hosted at "https://viv-demo.storage.googleapis.com/LuCa-7color_Scan1/"
render(image_location=urlparse("https://viv-demo.storage.googleapis.com/LuCa-7color_Scan1/"))

# Embeds an IFrame of a static build of Polus Render with an image hosted locally at "C:\Users\JeffChen\OneDrive - Axle Informatics\Documents\zarr files\pyramid.zarr"
render(image_location=Path(r"C:\Users\JeffChen\OneDrive - Axle Informatics\Documents\zarr files\pyramid.zarr"))

# Embeds an IFrame of a static build of Polus Render with an image and overlay file that is hosted locally
render(image_location=Path(r"C:\Users\JeffChen\OneDrive - Axle Informatics\Documents\zarr files\pyramid.zarr"), \
microjson_overlay_location=Path(r"C:\Users\JeffChen\OneDrive - Axle Informatics\Documents\overlay files\x00_y01_c1_segmentations.json"))

# Embeds an IFrame of a static build of Polus Render with an image and overlay file that is hosted online
render(image_location=urlparse("https://files.scb-ncats.io/pyramids/segmentations/x00_y01_c1.ome.tif"), \
microjson_overlay_location=urlparse("https://files.scb-ncats.io/pyramids/segmentations/x00_y03_c1_segmentations.json"))

# Embeds an IFrame with a height of 1080 of a local build of Polus Render.
render(height=1080)

# Embeds an IFrame into remote JupyterLab notebook. Use this function with argument nbhub_url to specify your notebooks url which must have lab in its url
nb_render(nbhub_url=urlparse("https://jh.scb-ncats.io/user/jeff.chen@axleinfo.com/user-namespaces/lab?"), image_location=Path("work/pyramid.zarr"))
```

# Functions
``` Python
def render(image_location:Union[ParseResult, PurePath] = "", microjson_overlay_location:Union[ParseResult, PurePath] = "", width:int=960, height:int=500, image_port:int=0, \
           microjson_overlay_port:int=0, use_local_render:bool=True, render_url:str = "https://render.ci.ncats.io/")->str:
    """
    Displays Polus Render with args to specify display dimensions, port to serve,
    image files to use, and overlay to use.
    
    Param:
        image_location(ParseResult|Purepath): Acquired from urllib.parse.ParseResult or Path, renders url in render.
                            If not specified, renders default render url.
        microjson_overlay_location(ParseResult|Purepath): Acquired from urllib.parse.ParseResult or Path, renders url in render.
                            If not specified, renders default render url
        width (int): width of render to be displayed, default is 960
        height (int): height of render to be displayed, default is 500
        image_port (int): Port to run local image server if used (default is 0 which is the 1st available port).
        microjson_overlay_port (int): Port to run local overlay server if used (default is 0 which is the 1st available port).
        use_local_render (bool): True to run local build of render with 1st available port, False to use render_url (default is True)
        render_url (str): URL which refers to Polus Render. Used when run_local_render is False. (default is https://render.ci.ncats.io/)
    Pre: zarr_port and json_port selected (if used) is not in use IF path given is Purepath
    Returns: Render URL
    """

def nb_render(nbhub_url:ParseResult,image_location:Union[ParseResult, PurePath] = "", microjson_overlay_location:Union[ParseResult, PurePath] = "", width:int=960, height:int=500, \
            use_local_render:bool=True, render_url:str = "https://render.ci.ncats.io/")->str:
    """
    Variant of render() used for remote jupyter notebooks. Read render() for usage information

    Param:
        nbhub_url: URL used used for jupyterhub. Contains '/lab/' in its uri
        image_location(ParseResult|Purepath): Acquired from urllib.parse.ParseResult or Path, renders url in render.
                            If not specified, renders default render url.
        microjson_overlay_location(ParseResult|Purepath): Acquired from urllib.parse.ParseResult or Path, renders url in render.
                            If not specified, renders default render url
        width (int): width of render to be displayed, default is 960
        height (int): height of render to be displayed, default is 500
        run_local_render (bool): True to run local build of render with 1st available port, False to use render_url (default is True)
        render_url (str): URL which refers to Polus Render. Used when run_local_render is False. (default is https://render.ci.ncats.io/)
    Returns: Render URL
    """
```

# Implementation Details
- Render application is loaded in an IFrame.
- render() and nb_render() builds up URL scheme fragments for render url, image url, and microjson url. It then combines url fragments into a single url which is displayed through an embedded IFrame.
- Static build of Polus Render as well as files to be displayed in nb_render() are served by Jupyter Server extension
- Dragging-and-dropping the dataset does not use a server. It calls an API from the front end (It should the this under the hood https://developer.mozilla.org/en-US/docs/Web/API/File_API).

# Misc Implementation Details
- Two type of servers are used.
>1. Python HTTPServer with CORS and OPTIONS functionality to serve RenderUI
>2. Modified UpDog Flask server to serve local files to RenderUI

# Acknowledgements
- UpDog: https://github.com/sc0tfree/updog
