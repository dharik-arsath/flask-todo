from dataclasses import dataclass

@dataclass
class TodoInfo:
    title           : str
    description     : str
    workspace       : str
    priority        : int
    id              : int   = -1

@dataclass
class WorkspaceInfo:
    user        : str
    title       : str
    description : str
    slug        : str
    url         : str