# Polus Render

Enables the embedding of content from polus-render within Jupyer notebooks.


![image](https://github.com/jcaxle/polus-render/assets/145499292/9ef28b98-3207-47d0-bdf9-207599239e3c)

## Requirements
* Python 3.9+

## Installation
TODO

## Sample usage
``` Python
from polus import render

# Embeds a render into Jupyter notebooks at https://render.ci.ncats.io/
render()
```

## Functions
``` Python
def render(path:ParseResult = None, width:int=960, height:int=500)->None:
    """
    Displays "https://render.ci.ncats.io/"
    
    Param:
        path (ParseResult): Acquired from urllib.parse.ParseResult, renders url in ParseResult 
                            If not specified, renders default url
        width (int): width of render to be displayed
        height (int): height of render to be displayed
    """
```
