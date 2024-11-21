import argparse
import os
import sys
from typing import Dict, Any

from pyqt6rc import __version__
from pyqt6rc.convert_tools import (
    ui_to_py,
    save_py,
    get_ui_files,
    update_resources,
    qrc_to_py,
    save_rcc_py,
    pyside6_qrc_to_pyqt6,
)
from pyqt6rc.script_helpers import set_logger

description = [
    f"pyqt6rc v{__version__}",
    "PyQt6 UI templates - Resource Converter.",
    "Default input location is Current Working Directory.",
    "",
    "Usage examples:",
    "  Convert all .ui files in CWD:",
    "  pyside6rc",
    "",
    "  Convert all .ui files in CWD, save output in different directory:",
    "  pyside6rc -o /directory/with/converted/templates",
    "",
]

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
    "-o",
    "--out",
    type=str,
    help="Output directory to save converted templates",
    default=None,
)
parser.add_argument("-s", "--silent", help="Supress logging", action="store_true")
parser.add_argument(
    "-npc",
    "--no-pyuic6-conversion",
    help="Don't convert .ui files to .py files.",
    action="store_true",
)
parser.add_argument(
    "-niw",
    "--no-import-write",
    help="Don't write import to converted ui files.",
    action="store_true",
)
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
    resources: Dict[str, Any] = {}
    converted_qrcs = []
    for input_file in input_files:
        current_resources = update_resources(input_file, resources)
        py_input = ui_to_py(input_file)
        injected_imports = []
        for qrc_info in current_resources["qrc_info"]:
            for info in qrc_info.values():
                if info["path"] not in converted_qrcs:
                    # Only do conversion once for same qrc file
                    qrc_input = qrc_to_py(info["path"])
                    qrc_input = pyside6_qrc_to_pyqt6(qrc_input)
                    converted_qrcs.append(info["path"])
                    save_rcc_py(info["path"], qrc_input)
                import_qrc = f"import {info['module_path']}.{info['import_as']}"
                if not args.no_import_write and import_qrc not in injected_imports:
                    # Only inject qrc import once
                    injected_imports.append(import_qrc)
                    py_input += "\n" + import_qrc + "  # noqa"
        if not args.no_pyuic6_conversion:
            save_py(input_file, py_input, args.out)
