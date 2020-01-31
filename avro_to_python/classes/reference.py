""" base Reference class """

from typing import Union


class Reference(object):

    def __init__(self, name: str, namespace: str):
        """
            Base struct on Reference Class
        """
        self.name = name
        self.namespace = namespace

    def __eq__(self, other: Union['Reference', str]):
        return self.name + self.namespace == other.name + other.namespace

    def __repr__(self):
        return f"<Reference:'{self.name}'>"
