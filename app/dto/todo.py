from dataclasses import dataclass

@dataclass
class TodoInfo:
    title           : str
    description     : str
    workspace       : str

@dataclass
class WorkspaceInfo:
    user        : str
    title       : str
    description : str
    url         : str