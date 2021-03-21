# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CircuitMap(Component):
    """A CircuitMap component.
Assumes horizontal stack

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- label (string; required): A label that will be printed when this component is rendered.
- value (dict; optional): The value displayed in the input.
- clickData (dict; optional): Data from latest click event. Read-only.
- hoverNodeData (dict; optional): Data of hovered node"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, label=Component.REQUIRED, value=Component.UNDEFINED, clickData=Component.UNDEFINED, hoverNodeData=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'label', 'value', 'clickData', 'hoverNodeData']
        self._type = 'CircuitMap'
        self._namespace = 'circuit_graph'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'label', 'value', 'clickData', 'hoverNodeData']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['label']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(CircuitMap, self).__init__(**args)
