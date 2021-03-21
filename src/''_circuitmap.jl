# AUTO GENERATED FILE - DO NOT EDIT

export ''_circuitmap

"""
    ''_circuitmap(;kwargs...)

A CircuitMap component.
Assumes horizontal stack
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `label` (String; required): A label that will be printed when this component is rendered.
- `value` (Dict; optional): The value displayed in the input.
- `clickData` (Dict; optional): Data from latest click event. Read-only.
- `hoverNodeData` (Dict; optional): Data of hovered node
"""
function ''_circuitmap(; kwargs...)
        available_props = Symbol[:id, :label, :value, :clickData, :hoverNodeData]
        wild_props = Symbol[]
        return Component("''_circuitmap", "CircuitMap", "circuit_graph", available_props, wild_props; kwargs...)
end

