# pyqt6rc

![GitHub_repo](https://img.shields.io/github/license/domarm-comat/pyqt6rc?style=for-the-badge)

Script to convert resource paths in files generated by pyuic6 command.  
PyQt6 does not provide pyrcc6 script to convert resources, that's the purpose of this package.  
In current PyQt6 implementation, py files created by pyuic6 script has wrong resource path.   
This script is converting .ui files into .py files and using importlib to fix resource path.

There are three major solutions to achieve correct path representation and resource usage, all covered by this package:

* Native >= python3.7 solution
  using [importlib](https://docs.python.org/3/library/importlib.html#module-importlib.resources) [**Use pyqt6rc**].
* Use of [importlib_resources](https://importlib-resources.readthedocs.io/en/latest/), for compatibility with
  Python3.6+ [**Use pyqt6rc with -c option**]
* Adding resource search path using QtCore.QDir.addSearchPath() and modifying generated prefixes [**Use pyqt6sp**]

More on this topic can be found on [StackOverflow](https://stackoverflow.com/questions/66099225/how-can-resources-be-provided-in-pyqt6-which-has-no-pyrcc).

In version 4.0, parameter -p, --package was removed. Pyqt6rc now determines package name automatically by crawling
parent folders and looking for \_\_init\_\_.py file.

# Conversion #

Generated template using pyuic6 script:

```python
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap(":/icons/icon1.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
```

Generated template using pyqt6rc script:

```python
from importlib.resources import path

icon = QtGui.QIcon()
with path("myPackage.resources.icons", "icon1.png") as f_path:
    icon.addPixmap(QtGui.QPixmap(str(f_path)), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
```

Generated template using pyqt6rc (-c, --compatible) script:

```python
from importlib_resources import path

icon = QtGui.QIcon()
with path("myPackage.resources.icons", "icon1.png") as f_path:
    icon.addPixmap(QtGui.QPixmap(str(f_path)), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
```

Generated template using pyqt6sp script:

```python
import os
from os.path import dirname, normpath
from PyQt6.QtCore import QDir

prefix_resources = [('icons', '../resources/')]
for prefix, resource in prefix_resources:
    sp = QDir.searchPaths(prefix)
    QDir.setSearchPaths(prefix, set(sp + [normpath(os.path.join(dirname(__file__), resource))]))

icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap("icons:icon1.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
```

# Usage examples #

Package structure example

```
myPackage
│   __init__.py    
│
└───resources
|   |   __init__.py
│   │   image1.png
│   │   image2.png
│   │   resources.qrc
|   |   ...
|   |
|   └───icons
│       │   __init__.py
│       │   icon1.png
│       │   icon2.png
│       │   ...
│   
└───templates
    │   template1.ui
    │   template2.ui
```

Batch convert all .ui files located in the templates directory

```shell
pyqt6rc /myPackage/templates
```

Convert template1.ui only

```shell
pyqt6rc /myPackage/templates/template1.ui
```

Convert template1.ui and save it in /tmp directory

```shell
pyqt6rc /myPackage/templates/template1.ui -o /tmp
```

Batch convert all .ui files located in templates directory using importlib_resources

```shell
pyqt6rc /myPackage/templates -c
```

Batch convert all .ui files located in templates directory using setSearchPaths method

```shell
pyqt6sp /myPackage/templates
```