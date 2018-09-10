"""
Crosscap, the Klein helper
"""
from collections import OrderedDict
import sys

import yaml

from crosscap import urltool, openapi
from crosscap.tree import openAPIDoc, enter
from crosscap._version import __version__
from crosscap.yamlhack import represent_ordered_dict


(urltool, openapi, openAPIDoc, enter, __version__) # for pyflakes


yaml.add_representer(openapi.OpenAPIParameter, openapi.representCleanOpenAPIParameter)
yaml.add_representer(openapi.OpenAPIResponse, openapi.representCleanOpenAPIObjects)
yaml.add_representer(openapi.OpenAPIResponses, openapi.representCleanOpenAPIObjects)
yaml.add_representer(openapi.OpenAPIMediaType, openapi.representCleanOpenAPIObjects)
yaml.add_representer(openapi.OpenAPIPathItem, openapi.representCleanOpenAPIPathItem)
yaml.add_representer(openapi.OpenAPIOperation, openapi.representCleanOpenAPIOperation)
yaml.add_representer(openapi.OpenAPI, openapi.representCleanOpenAPIObjects)
yaml.add_representer(openapi.OpenAPIInfo, openapi.representCleanOpenAPIObjects)
yaml.add_representer(OrderedDict, represent_ordered_dict)

if sys.version_info.major == 3: # pragma: nocover
    yaml.add_representer(str, urltool.literal_unicode_representer)
else: # pragma: nocover
    yaml.add_representer(type(u''), urltool.literal_unicode_representer)

yaml.add_representer(bytes, urltool.literal_unicode_representer)


__all__ = '__version__ openapi urltool openAPIDoc enter'.split()
