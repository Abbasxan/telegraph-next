from typing import Optional, List, Union

from pydantic import BaseModel


class Node(BaseModel):
    """ This abstract object represents a DOM Node. """
    tag: str
    """ Name of the DOM element. """
    attrs: Optional[dict] = None
    """ Optional. Attributes of the DOM element """
    children: Optional[List[Union[str, "Node"]]] = None
    """ Optional. List of child nodes for the DOM element. """


Node.model_rebuild()
