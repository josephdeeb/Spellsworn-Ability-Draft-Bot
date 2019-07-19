import Object.py
import abc

"""
'Event' represents
id : identification number of the event
name : name of the event
"""
class Event:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    """
    performEvent is the method that actually performs the event between the actors.
    Each actor's relationship to one another, if necessary for execution, is in the matrix.
    actors : list of all actors that are involved in execution of the event
    matrix : 2d matrix of all actors and their relationship with each other actor
    """
    @abc.abstractmethod
    def performEvent(self, actors, matrix):
        raise NotImplementedError("Users must define performEvent to use this base class")
