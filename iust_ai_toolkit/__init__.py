import importlib

from . import cli
from .abdi_4031 import decision_tree_submission


def course_module(module_name: str):
    """Dynamically import a module and return its functions."""
    module = importlib.import_module("iust_ai_toolkit." + module_name)
    return module


name = "iust_ai_toolkit"
