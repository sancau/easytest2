#-*- coding: utf8 -*-
"""
Commonly used util methods
"""


def json_handler(obj):
 	if hasattr(obj, 'isoformat'):
 		return obj.isoformat()
 	else:
 		raise TypeError({'obj': obj, 'type': type(obj)})
