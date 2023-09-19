from IPython.display import display, IFrame
from urllib.parse import ParseResult


def render(path:ParseResult = None, width:int=960, height:int=500)->None:
    """
    Displays "https://render.ci.ncats.io/"
    
    Param:
        path (ParseResult): Acquired from urllib.parse.ParseResult, renders url in ParseResult 
                            If not specified, renders default url
        width (int): width of render to be displayed
        height (int): height of render to be displayed
        
    """
    # Extract url if it exists
    url = None
    if path:
        url = path.geturl() # Can be manually rebuilt to check if a valid format url is sent
    
    # Display render
    display(IFrame(src=("https://render.ci.ncats.io/" if not url else 
                                                        "https://render.ci.ncats.io/?imageUrl=" + url)
                                                        , width=width, height=height))
    