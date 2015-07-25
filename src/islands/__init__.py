from .base import island_netloc_table, island_class_table, IslandNotDetectError
import glob
import os.path
__author__ = 'zz'


modules = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [os.path.basename(m)[:-3] for m in modules]


from . import *


