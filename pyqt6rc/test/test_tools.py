import os.path

import pytest

from pyqt6rc.tools import parse_qrc, ui_to_py, modify_py, get_ui_files, save_py


def test_qrc_parse() -> None:
    parsed_qrc = parse_qrc("pyqt6rc/test/resources.qrc")
    assert parsed_qrc == {'//': {},
                          '/icons': {},
                          '/subdir/icons/': {},
                          '/subdir/icons_aliased/': {'test.png': 'aliased.png'}} != {'/icons': {}, '/subdir/icons/': {}}


def test_broken_qrc_parse() -> None:
    with pytest.raises(Exception):
        parse_qrc("pyqt6rc/test/broken_resources.qrc")


def test_conversion() -> None:
    parsed_qrc = parse_qrc("pyqt6rc/test/myPackage/resources/resources.qrc")
    convert_ui_to_py = ui_to_py("pyqt6rc/test/myPackage/templates/template1.ui")
    modified_py = modify_py("myPackage.resources", convert_ui_to_py, parsed_qrc)

    with open("pyqt6rc/test/myPackage/templates/template1_reference.py", "r") as fp:
        assert fp.read() == modified_py


def test_get_ui_files():
    ui_files = get_ui_files("pyqt6rc/test/myPackage/templates")
    assert ui_files == ['pyqt6rc/test/myPackage/templates/template2.ui', 'pyqt6rc/test/myPackage/templates/template1.ui']


def test_save_py():
    parsed_qrc = parse_qrc("pyqt6rc/test/myPackage/resources/resources.qrc")
    convert_ui_to_py = ui_to_py("pyqt6rc/test/myPackage/templates/template1.ui")
    modified_py = modify_py("myPackage.resources", convert_ui_to_py, parsed_qrc)

    save_py("pyqt6rc/test/myPackage/templates/template1.ui", modified_py, "pyqt6rc/test/")
    assert os.path.isfile("pyqt6rc/test/template1.py")

    try:
        with open("pyqt6rc/test/template1.py", "r") as fp:
            assert fp.read() == modified_py
    finally:
        os.remove("pyqt6rc/test/template1.py")