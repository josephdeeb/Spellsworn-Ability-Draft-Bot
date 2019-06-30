import abc

"""
Represents an interactable object in the game world.
id: identification number of the object
name: name of the object
validActions: dictionary which contains True or False values for each potential action (isExamineable, isTakeable, etc.)
"""
class Object:
    def __init__(self, id, name, validActions):
        self.id = id
        self.name = name
        self.validActions = validActions

    def copyValidActions(self):
        copy = dict()
        for key, value in self.validActions:
            copy[key] = value
        return copy

    def getId(self):
        return self.id

    def getName(self):
        return self.name


class Examineable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getExamineEvent(self):
        raise NotImplementedError("Users must define getExamineEvent to use this base class")

class Takeable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getTakeableEvent(self):
        raise NotImplementedError("Users must define getTakeableEvent to use this base class")


class ExamineableDefault(Examineable):
    def getExamineText(self):


class EnvironmentFeature(Object, Examineable):
    def __init__(self, id, name, validActions):
        Object.__init__(self, id, name, validActions)
