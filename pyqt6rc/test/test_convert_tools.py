import os.path

import pytest

from pyqt6rc.convert_tools import parse_qrc, ui_to_py, modify_py, get_ui_files, save_py, update_resources


def test_qrc_parse() -> None:
    parsed_qrc = parse_qrc("pyqt6rc/test/resources.qrc")
    assert parsed_qrc == {'/': {'aliases': {}, 'package': 'test'},
                          '/icons/': {'aliases': {}, 'package': 'test'},
                          '/subdir/icons/': {'aliases': {}, 'package': 'test'},
                          '/subdir/icons_aliased/': {'aliases': {'test.png': 'aliased.png'},
                                                     'package': 'test'}}


def test_broken_qrc_parse() -> None:
    with pytest.raises(Exception):
        parse_qrc("pyqt6rc/test/broken_resources.qrc")


@pytest.mark.parametrize("compatible", [False, True])
def test_conversion(compatible) -> None:
    reference_file = "template1_reference_compatible.py" if compatible else "template1_reference.py"

    resources = {}
    update_resources("pyqt6rc/test/myPackage/templates/template1.ui", resources)
    convert_ui_to_py = ui_to_py("pyqt6rc/test/myPackage/templates/template1.ui")
    modified_py = modify_py("myPackage", convert_ui_to_py, resources, compatible=compatible)

    with open(f"pyqt6rc/test/myPackage/templates/{reference_file}", "r") as fp:
        assert fp.read().split("\n", 6)[2] == modified_py.split("\n", 6)[2]


def test_get_ui_files():
    ui_files = get_ui_files("pyqt6rc/test/myPackage/templates")
    assert ui_files == ['pyqt6rc/test/myPackage/templates/template2.ui',
                        'pyqt6rc/test/myPackage/templates/template1.ui']


def test_save_py():
    parsed_qrc = parse_qrc("pyqt6rc/test/myPackage/resources/resources.qrc")
    for template_name in ("template1", "template2"):
        convert_ui_to_py = ui_to_py(f"pyqt6rc/test/myPackage/templates/{template_name}.ui")
        modified_py = modify_py("myPackage.resources", convert_ui_to_py, parsed_qrc)

        save_py(f"pyqt6rc/test/myPackage/templates/{template_name}.ui", modified_py, "pyqt6rc/test/")
        assert os.path.isfile(f"pyqt6rc/test/{template_name}.py")

        try:
            with open(f"pyqt6rc/test/{template_name}.py", "r") as fp:
                assert fp.read().split("\n", 6)[2] == modified_py.split("\n", 6)[2]
        finally:
            os.remove(f"pyqt6rc/test/{template_name}.py")
