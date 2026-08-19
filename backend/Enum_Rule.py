#!/usr/bin/python3

from enum import Enum, auto

class Rule(Enum):  
    DOCUMENT    = auto()
    BLOCK       = auto()
    HEADING     = auto()
    LIST        = auto()
    LIST_NUM    = auto()
    LIST_ITEM   = auto()
    PARAGRAPH   = auto()
    INLINE      = auto()
    H_LINE      = auto()
    IMAGE       = auto()
    LINK        = auto()
    QUOTE       = auto()
    TABLE       = auto()
    CODE_BLOCK  = auto()
    CODE_INLINE = auto()
    NEW_LINE    = auto()
    EOF         = auto()
