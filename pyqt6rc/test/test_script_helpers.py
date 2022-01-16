import logging

import pytest

from pyqt6rc.script_helpers import set_logger


@pytest.mark.parametrize("disabled", [False, True])
def test_set_logger(disabled, caplog, request) -> None:
    test_id = request.node.callspec.id
    set_logger(disabled)
    logging.info("test")
    if test_id == "True":
        assert caplog.messages == []
    else:
        assert caplog.messages == ["test"]
