import os.path
from typing import Dict, Any

import pytest

from pyqt6rc.convert_tools import (
    parse_qrc,
    ui_to_py,
    modify_py,
    get_ui_files,
    save_py,
    update_resources,
    modify_py_sp,
    update_resources_sp,
    pyside6_qrc_to_pyqt6,
)


def test_qrc_parse() -> None:
    parsed_qrc = parse_qrc("pyqt6rc/test/test_resources/resources.qrc")
    assert parsed_qrc == {
        "/": {
            "module_path": "",
            "aliases": {},
            "path": "pyqt6rc/test/test_resources/resources.qrc",
            "basename": "resources.qrc",
            "import_as": "resources",
        },
        "/icons/": {
            "module_path": "",
            "aliases": {},
            "path": "pyqt6rc/test/test_resources/resources.qrc",
            "basename": "resources.qrc",
            "import_as": "resources",
        },
        "/subdir/icons/": {
            "module_path": "",
            "aliases": {},
            "path": "pyqt6rc/test/test_resources/resources.qrc",
            "basename": "resources.qrc",
            "import_as": "resources",
        },
        "/subdir/icons_aliased/": {
            "module_path": "",
            "aliases": {"test.png": "aliased.png"},
            "path": "pyqt6rc/test/test_resources/resources.qrc",
            "basename": "resources.qrc",
            "import_as": "resources",
        },
    }


def test_broken_qrc_parse() -> None:
    with pytest.raises(Exception):
        parse_qrc("pyqt6rc/test/test_resources/broken_resources.qrc")


@pytest.mark.parametrize("compatible", [False, True])
def test_conversion(compatible: bool) -> None:
    reference_file = (
        "template1_reference_compatible.py" if compatible else "template1_reference.py"
    )

    resources: Dict[str, Any] = {}
    update_resources(
        "pyqt6rc/test/test_resources/myPackage/templates/template1.ui", resources
    )
    convert_ui_to_py = ui_to_py(
        "pyqt6rc/test/test_resources/myPackage/templates/template1.ui"
    )
    modified_py = modify_py(convert_ui_to_py, resources, compatible=compatible)

    with open(
        f"pyqt6rc/test/test_resources/myPackage/templates/{reference_file}",
        "r",
        encoding="utf-8",
    ) as fp:
        assert fp.read().split("\n", 6)[5] == modified_py.split("\n", 6)[5]


def test_sp_conversion() -> None:
    reference_file = "template1_sp_reference.py"

    resources: Dict[str, Any] = {}
    resource_rel_path = update_resources_sp(
        "pyqt6rc/test/test_resources/myPackage/templates/template1.ui", resources
    )
    convert_ui_to_py = ui_to_py(
        "pyqt6rc/test/test_resources/myPackage/templates/template1.ui"
    )
    modified_py = modify_py_sp(convert_ui_to_py, resources, resource_rel_path)

    with open(
        f"pyqt6rc/test/test_resources/myPackage/templates/{reference_file}",
        "r",
        encoding="utf-8",
    ) as fp:
        assert fp.read().split("\n", 6)[5] == modified_py.split("\n", 6)[5]


def test_sp_conversion_no_resources() -> None:
    reference_file = "template3_reference.py"

    resources: Dict[str, Any] = {}
    resource_rel_path = update_resources_sp(
        "pyqt6rc/test/test_resources/myPackage/templates/template3.ui", resources
    )
    convert_ui_to_py = ui_to_py(
        "pyqt6rc/test/test_resources/myPackage/templates/template3.ui"
    )
    modified_py = modify_py_sp(convert_ui_to_py, resources, resource_rel_path)

    with open(
        f"pyqt6rc/test/test_resources/myPackage/templates/{reference_file}",
        "r",
        encoding="utf-8",
    ) as fp:
        assert fp.read().split("\n", 6)[5] == modified_py.split("\n", 6)[5]


def test_get_ui_files() -> None:
    ui_files = get_ui_files("pyqt6rc/test/test_resources/myPackage/templates")
    assert "pyqt6rc/test/test_resources/myPackage/templates/template3.ui" in ui_files
    assert "pyqt6rc/test/test_resources/myPackage/templates/template2.ui" in ui_files
    assert "pyqt6rc/test/test_resources/myPackage/templates/template1.ui" in ui_files


def test_save_py() -> None:
    parsed_qrc = parse_qrc(
        "pyqt6rc/test/test_resources/myPackage/resources/resources.qrc"
    )
    for template_name in ("template1", "template2"):
        convert_ui_to_py = ui_to_py(
            f"pyqt6rc/test/test_resources/myPackage/templates/{template_name}.ui"
        )
        modified_py = modify_py(convert_ui_to_py, parsed_qrc)

        save_py(
            f"pyqt6rc/test/test_resources/myPackage/templates/{template_name}.ui",
            modified_py,
            "pyqt6rc/test/",
        )
        assert os.path.isfile(f"pyqt6rc/test/{template_name}.py")

        try:
            with open(f"pyqt6rc/test/{template_name}.py", "r", encoding="utf-8") as fp:
                assert fp.read().split("\n", 6)[5] == modified_py.split("\n", 6)[5]
        finally:
            os.remove(f"pyqt6rc/test/{template_name}.py")


def test_pyside6_qrc_to_pyqt6() -> None:
    reference_file = "pyqt6_resources.py"
    with open(
        "pyqt6rc/test/test_resources/myPackage/resources/pyside_resources.py",
        "r",
        encoding="utf-8",
    ) as fp:
        pyside_py_qrc_input = fp.read()

    converted_qrc = pyside6_qrc_to_pyqt6(pyside_py_qrc_input)
    with open(
        f"pyqt6rc/test/test_resources/myPackage/resources/{reference_file}",
        "r",
        encoding="utf-8",
    ) as fp:
        assert fp.read() == converted_qrc
