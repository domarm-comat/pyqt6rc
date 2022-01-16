import re

__version__ = "0.3.1"

resource_pattern = re.compile('":(\/.*?\.[\w:]+)"')
indent_pattern = re.compile('\s+')
