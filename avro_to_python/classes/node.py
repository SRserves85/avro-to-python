""" base node class for tree structure """

from typing import Union


class Node(object):

    def __init__(self, name: str, children: dict={}, files: dict={},
                 visited: bool=False):
        """
            Base struct on Node Class
        """
        self.name = name
        self.children = children
        self.files = files
        self.visited = visited

    def __eq__(self, other: Union['Node', str]):
        if isinstance(other, Node):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other

    def __repr__(self):
        return f"<Node:'{self.name}'>"
