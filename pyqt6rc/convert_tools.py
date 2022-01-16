import logging
import os
import xml.etree.ElementTree as Et
from os.path import dirname, basename
from typing import List, Optional, Dict

from pyqt6rc import resource_pattern, indent_pattern


def parse_qrc(qrc_file: str) -> dict:
    """
    Parse qrc xml file and extract prefixes and aliases.
    :param str qrc_file: path to qrc_file
    :return dict: parsed qrc
    """
    tree = Et.parse(qrc_file)
    root = tree.getroot()

    if root.tag != "RCC":
        raise Exception(f"Invalid Resource file format.")

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
            resources[prefix] = {
                "package": os.path.basename(os.path.dirname(qrc_file)),
                "aliases": aliases
            }
    return resources


def update_resources(ui_file: str, resources: Dict) -> None:
    """
    Read ui file and collect all input resource files.
    :param str ui_file: input ui template
    :param dict resources: input parsed resources
    :return:
    """
    tree = Et.parse(ui_file)
    root = tree.getroot()

    if root.tag != "ui":
        raise Exception(f"Invalid template file format.")

    ui_dir = os.path.dirname(ui_file)
    for child in root:
        if child.tag == "resources":
            for include in child:
                location = include.attrib.get("location", None)
                if location is not None:
                    resource_location = os.path.normpath(os.path.join(ui_dir, location))
                    resources.update(parse_qrc(resource_location))


def ui_to_py(ui_file: str) -> str:
    """
    Use pyuic6 to convert ui template into py file
    :param str ui_file: input ui template file
    :return str: converted python template
    """
    return os.popen(f"pyuic6 {ui_file}").read()


def modify_py(package: str, py_input: str, resources: dict, tab_size: int = 4) -> str:
    """
    Modify python template, wrap resource files with path(resource_package, f_name) as f_path.
    :param str package: resource package
    :param str py_input: converted python template
    :param dict resources: collected resources
    :param int tab_size: number of spaces in one tab
    :return str: modified python template
    """
    output = ""
    imported = False
    tab = " " * tab_size

    for line in py_input.split("\n"):
        # Check if path was imported
        if not imported and line.startswith("from"):
            output += "from importlib.resources import path\n"
            imported = True
        # Check if any resource path is in line
        out = resource_pattern.search(line)
        if out is not None:
            tabs = indent_pattern.search(line)
            sub_package, path = None, None
            # Check if resource path starts with any of the prefixes
            for prefix in resources.keys():
                if out[1].startswith(prefix):
                    # make file path by removing prefix from it
                    sub_package = resources[prefix]["package"]
                    path = out[1][len(prefix):]
                    break
            if path is None:
                # Prefix doesn't exist in qrc file, comment out that line
                logging.warning(f"Prefix \"{out[1].split('/')[1]}\" not found in qrc file.")
                output += "# " + line + "\n"
                continue

            # Split file path into parts
            path_parts = list(filter(None, dirname(path).split("/")))
            # Make final resource_package name
            resource_package = ".".join([package, sub_package] + path_parts)
            # Get file name
            f_name = basename(out[1])
            output += f"{tabs[0]}with path(\"{resource_package}\", \"{f_name}\") as f_path:\n"
            line = tab + line.replace(out[0], f"str(f_path)")

        # Append new line into output
        output += line + "\n"
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
    with open(output_filename_path, "w") as fp:
        fp.write(py_input)
    logging.info(f"{input_filename} > {output_filename}")


def get_ui_files(input_dir: str) -> List[str]:
    """
    Get all .ui template files in input directory
    :param str input_dir:input directory
    :return list: list of .ui files
    """
    files = []
    for entry in os.scandir(input_dir):
        if entry.is_file(follow_symlinks=False) and entry.name.endswith(".ui"):
            files.append(entry.path)
    logging.info(f"Found {len(files)} .ui files")
    return files
