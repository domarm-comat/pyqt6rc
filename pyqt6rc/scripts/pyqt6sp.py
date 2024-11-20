import argparse
import os
import sys
from typing import Any, Dict

from pyqt6rc import __version__
from pyqt6rc.convert_tools import (
    ui_to_py,
    save_py,
    get_ui_files,
    modify_py_sp,
    update_resources_sp,
)
from pyqt6rc.script_helpers import set_logger

description = [
    f"pyqt6rc v{__version__}",
    "PyQt6 UI templates - Set search Paths.",
    "Default input location is Current Working Directory.",
    "",
    "Usage examples:",
    "  Convert all .ui files in CWD:",
    "  pyqt6sp",
    "",
    "  Convert all .ui files in directory:",
    "  pyqt6sp -i /directory/with/templates",
    "",
    "  Convert all .ui files in CWD, save output in different directory:",
    "  pyqt6sp -o /directory/with/converted/templates",
    "",
]

"""
from os.path import basename, dirname, normpath
from PyQt6.QtCore import QDir

prefix_resources = [("icons", "../resources")]
for prefix, resource in prefix_resources:
    sp = QDir.searchPaths(prefix)
    QDir.setSearchPaths(prefix, set(sp + [normpath(os.path.join(dirname(__file__), resource))]))
"""

arguments = sys.argv
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter, description="\r\n".join(description)
)
parser.add_argument(
    "input",
    type=str,
    help="Path to .ui template file or Directory containing .ui files."
    "If empty, scan current working directory and use all .ui template files.",
    default="*",
    nargs="?",
)
parser.add_argument(
    "-tb", "--tab_size", type=int, help="Size of tab in spaces, default=4", default=4
)
parser.add_argument(
    "-o",
    "--out",
    type=str,
    help="Output directory to save converted templates",
    default=None,
)
parser.add_argument("-s", "--silent", help="Supress logging", action="store_true")
args = parser.parse_args()

# Set logger
set_logger(args.silent)

# Input files check
if args.input == "*":
    input_files = get_ui_files(os.getcwd())
elif os.path.isdir(args.input):
    input_files = get_ui_files(args.input)
else:
    if not args.input.endswith(".ui"):
        raise Exception(f"Not template file {args.input}.")
    if not os.path.exists(args.input):
        raise Exception(f"Template file {args.input} does not exists.")
    input_files = [args.input]


def run() -> None:
    for input_file in input_files:
        resources: Dict[str, Any] = {}
        resource_rel_path = update_resources_sp(input_file, resources)
        py_input = ui_to_py(input_file)
        py_input = modify_py_sp(py_input, resources, resource_rel_path, args.tab_size)
        save_py(input_file, py_input, args.out)
