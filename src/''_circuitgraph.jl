# AUTO GENERATED FILE - DO NOT EDIT

export ''_circuitgraph

"""
    ''_circuitgraph(;kwargs...)

A CircuitGraph component.
Assumes horizontal stack
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `label` (String; required): A label that will be printed when this component is rendered.
- `value` (Dict; optional): The value displayed in the input.
- `clickData` (Dict; optional): Data from latest click event. Read-only.
- `mapData` (Real; optional): Data from latest click event. Read-only.
"""
function ''_circuitgraph(; kwargs...)
        available_props = Symbol[:id, :label, :value, :clickData, :mapData]
        wild_props = Symbol[]
        return Component("''_circuitgraph", "CircuitGraph", "circuit_graph", available_props, wild_props; kwargs...)
end

