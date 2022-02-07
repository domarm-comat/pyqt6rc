# pyqt6rc

![GitHub_repo](https://img.shields.io/github/license/domarm-comat/pyqt6rc?style=for-the-badge)

Script to convert resource paths generated by QT6 designer.  
PyQt6 does not provide pyrcc6 script to convert resources.  
In current PyQt6 implementation, files created by pyuic6 scripts using Qt resources has wrong path.   
This script is converting .ui files into .py files and using importlib to fix resource path.

There are three major solutions to this problem, all covered by this package:
* Native python3.7+ solution using [importlib](https://docs.python.org/3/library/importlib.html#module-importlib.resources) [**Use pyqt6rc**].
* Use of [importlib_resources](https://importlib-resources.readthedocs.io/en/latest/), for compatibility with Python3.6+ [**Use pyqt6rc with -c option**]
* Adding resource search path using QtCore.QDir.addSearchPath() and modifying generated prefixes [**Use pyqt6sp**]

# Conversion #

Generated template using pyuic6:
```python
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap(":/icons/icon1.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
```

Generated template using pyqt6rc:
```python
from importlib.resources import path

icon = QtGui.QIcon()
with path("myPackage.resources.icons", "icon1.png") as f_path:
    icon.addPixmap(QtGui.QPixmap(str(f_path)), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
```

Generated template using pyqt6rc (-c, --compatible):
```python
from importlib_resources import path

icon = QtGui.QIcon()
with path("myPackage.resources.icons", "icon1.png") as f_path:
    icon.addPixmap(QtGui.QPixmap(str(f_path)), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
```

Generated template using pyqt6sp:
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

Convert all .ui files located in templates directory
```shell
pyqt6rc /myPackage/templates -p myPackage
```

Convert template1.ui
```shell
pyqt6rc /myPackage/templates/template1.ui -p myPackage
```

Convert template1.ui and save it in /tmp directory
```shell
pyqt6rc /myPackage/templates/template1.ui -p myPackage -o /tmp
```

Convert all .ui files located in templates directory using importlib_resources
```shell
pyqt6rc /myPackage/templates -p myPackage -c
```

Convert all .ui files located in templates directory using setSearchPaths method
```shell
pyqt6sp /myPackage/templates
```