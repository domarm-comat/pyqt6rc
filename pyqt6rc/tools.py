import os
import re
import xml.etree.ElementTree as Et
from os.path import dirname, basename

from pyqt6rc import resource_pattern, indent_pattern


def parse_qrc(qrc_file):
    tree = Et.parse(qrc_file)
    root = tree.getroot()

    if root.tag != "RCC":
        raise Exception(f"Invalid Resource file format.")

    # Read resource tree
    tree = {}
    for child in root:
        if child.tag == "qresource":
            files = []
            for file_child in child:
                files.append((file_child.attrib.get("alias", ""), file_child.text))
            tree["/" + child.attrib.get("prefix", "")] = files

    return tree


def ui_to_py(ui_file):
    return os.popen(f"pyuic6 {ui_file}").read()


def modify_py(package, py_input, qrc, tab_size=4):
    output = ""
    included = False
    tab = " " * tab_size

    for line in py_input.split("\n"):
        out = resource_pattern.search(line)
        if not included and line.startswith("from"):
            output += "from importlib.resources import path\n"
            included = True
        if out is not None:
            tabs = indent_pattern.search(line)
            path = "/"
            for prefix in qrc.keys():
                if out[1].startswith(prefix):
                    path = out[1][len(prefix):]
                    break
            path_parts = list(filter(None, dirname(path).split("/")))
            pckg = ".".join([package] + list(path_parts))
            f_name = basename(out[1])
            output += f"{tabs[0]}with path(\"{pckg}\", \"{f_name}\") as f_path:\n"
            line = tab + line.replace(out[0], f"str(f_path)")

        output += line + "\n"
    return output

def save_py(ui_file, py_input):
    parts = ui_file.split(".")
    parts[-1] = "py"
    with open(".".join(parts), "w") as fp:
        fp.write(py_input)
