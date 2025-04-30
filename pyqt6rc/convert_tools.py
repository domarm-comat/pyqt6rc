import logging
import os
import subprocess
import xml.etree.ElementTree as Et
from os.path import dirname, basename
from pathlib import Path
from typing import List, Optional, Dict, Any
from pyqt6rc import resource_pattern, indent_pattern


def get_module_path(input_dir: str) -> str:
    """
    Get module path by crawling parent folders and looking for __init__.py file.
    Last folder having __init__.py is top-level package name.
    :param str input_dir: input directory
    :return: module path
    """
    package_parts: List[str] = []
    while True:
        try:
            for entry in os.scandir(input_dir):
                if entry.name == "__init__.py":
                    package_parts.insert(0, os.path.basename(input_dir))
                    input_dir = os.path.dirname(input_dir)
                    break
            else:
                break
        except FileNotFoundError:
            break
    return ".".join(package_parts)


def parse_qrc(qrc_file: str) -> Dict[str, Any]:
    """
    Parse qrc xml file and extract prefixes and aliases.
    :param str qrc_file: path to qrc_file
    :return dict: parsed qrc
    """
    tree = Et.parse(qrc_file)
    root = tree.getroot()

    if root.tag != "RCC":
        raise Exception("Invalid Resource file format.")

    resources = {}
    for child in root:
        if child.tag == "qresource":
            aliases = {}
            for file_child in child:
                alias = file_child.attrib.get("alias", None)
                if alias is not None:
                    aliases[file_child.text] = alias
            prefix = "/" + child.attrib.get("prefix", "")
            if not prefix.endswith("/"):
                prefix += "/"

            basename = os.path.basename(qrc_file)
            resources[prefix] = {
                "module_path": get_module_path(os.path.dirname(qrc_file)),
                "aliases": aliases,
                "path": qrc_file,
                "basename": basename,
                "import_as": Path(basename).stem,
            }
    return resources


def update_resources(
    ui_file: str, resources: Dict[str, Any]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Read ui file and collect all input resource files.
    :param str ui_file: input ui template
    :param dict resources: input parsed resources
    :return:
    """
    tree = Et.parse(ui_file)
    root = tree.getroot()

    if root.tag != "ui":
        raise Exception("Invalid template file format.")

    ui_dir = os.path.dirname(ui_file)
    current_resources: Dict[str, List[Dict[str, Any]]] = {"qrc_info": []}
    for child in root:
        if child.tag == "resources":
            for include in child:
                location = include.attrib.get("location", None)
                if location is not None:
                    resource_location = os.path.normpath(os.path.join(ui_dir, location))
                    qrc_info = parse_qrc(resource_location)
                    resources.update(qrc_info)
                    current_resources["qrc_info"].append(qrc_info)
    return current_resources


def update_resources_sp(ui_file: str, resources: Dict[str, Any]) -> str:
    """
    Read ui file and collect all input resource files.
    :param str ui_file: input ui template
    :param dict resources: input parsed resources
    :return:
    """
    tree = Et.parse(ui_file)
    root = tree.getroot()

    if root.tag != "ui":
        raise Exception("Invalid template file format.")

    ui_dir = os.path.dirname(ui_file)
    location = None
    for child in root:
        if child.tag == "resources":
            for include in child:
                location = include.attrib.get("location", None)
                if location is not None:
                    resource_location = os.path.normpath(os.path.join(ui_dir, location))
                    resources.update(parse_qrc(resource_location))
    return dirname(location) if location is not None else ""


def qrc_to_py(qrc_file: str) -> str:
    return subprocess.check_output(
        ["pyside6-rcc", qrc_file], universal_newlines=True, encoding="utf-8"
    )


def pyside6_qrc_to_pyqt6(qrc_input: str) -> str:
    return qrc_input.replace("PySide6", "PyQt6")


def save_rcc_py(qrc_file: str, py_input: str) -> None:
    """
    Save python template into file.
    Use ui filename and change .ui suffix to .py.
    If output_dir is None, use same dir as a .ui template file to store converted .py template.
    :param str qrc_file: input ui template file
    :param str py_input: converted python template
    :param str output_dir: output directory
    :return: None
    """
    input_filename = os.path.basename(qrc_file)
    parts = input_filename.split(".")
    parts[-1] = "py"
    output_dir = os.path.dirname(qrc_file)
    output_filename = ".".join(parts)
    output_filename_path = os.path.join(output_dir, output_filename)
    with open(output_filename_path, "w", encoding="utf-8") as fp:
        fp.write(py_input)
    logging.info(f"{input_filename} > {output_filename}")


def ui_to_py(ui_file: str) -> str:
    """
    Use pyuic6 to convert ui template into py file
    :param str ui_file: input ui template file
    :return str: converted python template
    """
    return subprocess.check_output(
        ["pyuic6", ui_file], universal_newlines=True, encoding="utf-8"
    )


def modify_py(
    py_input: str,
    resources: Dict[str, Any],
    tab_size: int = 4,
    compatible: bool = False,
) -> str:
    """
    Modify python template, wrap resource files with path(resource_package, f_name) as f_path.
    :param str py_input: converted python template
    :param dict resources: collected resources
    :param int tab_size: number of spaces in one tab
    :param bool compatible: use compatible importlib_resources instead of native importlib
    :return str: modified python template
    """
    output = ""
    imported = False
    tab = " " * tab_size

    for line in py_input.split("\n"):
        # Check if path was imported
        if not imported and line.startswith("from"):
            if compatible:
                output += "from importlib_resources import path\n"
            else:
                output += "from importlib.resources import path\n"
            imported = True
        # Check if any resource path is in line
        out = resource_pattern.search(line)
        if out is not None:
            tabs = indent_pattern.search(line)
            package, path = None, None
            # Check if resource path starts with any of the prefixes
            for prefix in resources.keys():
                if out[1].startswith(prefix):
                    # make file path by removing prefix from it
                    package = resources[prefix].get("module_path")
                    prefix_len = len(prefix)
                    path = out[1][prefix_len:]
                    break
            if path is None:
                # Prefix doesn't exist in qrc file, comment out that line
                logging.warning(
                    f"Prefix \"{out[1].split('/')[1]}\" not found in qrc file."
                )
                output += "# " + line + "\n"
                continue
            if package is None:
                raise Exception("Package name is empty")

            # Split file path into parts
            path_parts = list(filter(None, dirname(path).split("/")))
            # Make final resource_package name
            resource_package = ".".join([package] + path_parts)

            # Get file name
            f_name = basename(out[1])
            tabs_offset = tabs[0] if tabs is not None else ""
            output += (
                f'{tabs_offset}with path("{resource_package}", "{f_name}") as f_path:\n'
            )
            line = tab + line.replace(out[0], "str(f_path)")

        # Append new line into output
        output += line + "\n"
    return output


def modify_py_sp(
    py_input: str, resources: Dict[str, Any], resource_rel_path: str, tab_size: int = 4
) -> str:
    """
    Modify python template, wrap resource files with path(resource_package, f_name) as f_path.
    :param str py_input: converted python template
    :param dict resources: collected resources
    :param str resource_rel_path: Relative path to the resource
    :param int tab_size: number of spaces in one tab
    :return str: modified python template
    """
    output = ""
    imported = False
    def_placeholder = False
    tab = " " * tab_size
    prefix_resources = set()
    placeholder = f"#{tab}__PLACEHOLDER__"
    if not resources:
        return py_input
    for index, line in enumerate(py_input.split("\n")):
        # Check if path was imported
        if not imported and line.startswith("from"):
            # Import all required packages
            output += (
                "import os\n"
                "from os.path import dirname, normpath\n"
                "from PyQt6.QtCore import QDir\n"
            )
            imported = True
        elif not def_placeholder and line.startswith(f"{tab}def setupUi"):
            # Append placeholder after setupUi definition
            line = line + "\n" + placeholder
            def_placeholder = True
        else:
            # Check if any resource path is in line
            out = resource_pattern.search(line)
            if out is not None:
                path, prefix = None, None
                # Check if resource path starts with any of the prefixes
                for prefix in resources.keys():
                    if out[1].startswith(prefix):
                        # make file path by removing prefix from it
                        prefix_len = len(prefix)
                        path = out[1][prefix_len:]
                        break
                if path is None or prefix is None:
                    # Prefix doesn't exist in qrc file, comment out that line
                    logging.warning(
                        f"Prefix \"{out[1].split('/')[1]}\" not found in qrc file."
                    )
                    output += "# " + line + "\n"
                    continue

                # Add prefix resource in format (prefix, resource_rel_path/filepath)
                prefix_resources.add(
                    (prefix[1:-1], "/".join([resource_rel_path, dirname(path)]))
                )
                # This creates file reference in format prefix:filename
                f_path = f"{prefix[1:-1]}:{basename(out[1])}"
                # Replace previous file reference of modified one
                line = line.replace(out[0], f'"{f_path}"')

        # Append new line into output
        output += line + "\n"
    # Generate code which setSearchPath for every prefix:resource
    # To get absolute dir path, combine current __filename__ dir, resource relative path and normalize it
    append_path_part = (
        f"{tab * 2}prefix_resources = {list(prefix_resources)}\n"
        f"{tab * 2}for prefix, resource in prefix_resources:\n"
        f"{tab * 3}sp = QDir.searchPaths(prefix)\n"
        f"{tab * 3}QDir.setSearchPaths(prefix, set(sp + [normpath(os.path.join(dirname(__file__), resource))]))\n"
    )
    output = output.replace(placeholder, append_path_part, 1)
    return output


def save_py(ui_file: str, py_input: str, output_dir: Optional[str] = None) -> None:
    """
    Save python template into file.
    Use ui filename and change .ui suffix to .py.
    If output_dir is None, use same dir as a .ui template file to store converted .py template.
    :param str ui_file: input ui template file
    :param str py_input: converted python template
    :param str output_dir: output directory
    :return: None
    """
    input_filename = os.path.basename(ui_file)
    parts = input_filename.split(".")
    parts[-1] = "py"

    if output_dir is None:
        output_dir = os.path.dirname(ui_file)
    else:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

    output_filename = ".".join(parts)
    output_filename_path = os.path.join(output_dir, output_filename)
    with open(output_filename_path, "w", encoding="utf-8") as fp:
        fp.write(py_input)
    logging.info(f"{input_filename} > {output_filename}")


def get_ui_files(input_dir: str) -> List[str]:
    """
    Get all .ui template files in input directory
    :param str input_dir: input directory
    :return list: list of .ui files
    """
    files = []
    for entry in os.scandir(input_dir):
        if entry.is_file(follow_symlinks=False) and entry.name.endswith(".ui"):
            files.append(os.path.normpath(entry.path))
    logging.info(f"Found {len(files)} .ui files")
    return files
