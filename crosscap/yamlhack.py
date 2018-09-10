"""
Make yaml respect OrderedDicts and stop sorting things
"""
from yaml.nodes import MappingNode, ScalarNode


def represent_ordered_dict(dumper, data):
    tag = u'tag:yaml.org,2002:map'
    mapping = data
    flow_style = False # I don't see any way to get this from the real dumper, so we'll hard code it

    value = []
    node = MappingNode(tag, value, flow_style=flow_style)
    if dumper.alias_key is not None:
        dumper.represented_objects[dumper.alias_key] = node
    best_style = True
    if hasattr(mapping, 'items'):
        mapping = mapping.items()
    for item_key, item_value in mapping:
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)
        if not (isinstance(node_key, ScalarNode) and not node_key.style):
            best_style = False
        if not (isinstance(node_value, ScalarNode) and not node_value.style):
            best_style = False
        value.append((node_key, node_value))
    if flow_style is None:
        if dumper.default_flow_style is not None:
            node.flow_style = dumper.default_flow_style
        else:
            node.flow_style = best_style
    return node
