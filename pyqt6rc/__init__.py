import re

__version__ = "0.7.0"

resource_pattern = re.compile(r'":(\/.*?\.[\w:]+)"')
indent_pattern = re.compile(r"\s+")
