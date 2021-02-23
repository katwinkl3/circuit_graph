# AUTO GENERATED FILE - DO NOT EDIT

export ''_circuitgraph

"""
    ''_circuitgraph(;kwargs...)

A CircuitGraph component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `label` (String; required): A label that will be printed when this component is rendered.
- `value` (Dict; optional): The value displayed in the input.
- `clickData` (Dict; optional): Data from latest click event. Read-only.
"""
function ''_circuitgraph(; kwargs...)
        available_props = Symbol[:id, :label, :value, :clickData]
        wild_props = Symbol[]
        return Component("''_circuitgraph", "CircuitGraph", "circuit_graph", available_props, wild_props; kwargs...)
end

