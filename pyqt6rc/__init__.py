import re

__version__ = "0.4.0"

resource_pattern = re.compile('":(\/.*?\.[\w:]+)"')
indent_pattern = re.compile('\s+')
