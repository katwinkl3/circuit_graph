# AUTO GENERATED FILE - DO NOT EDIT

''CircuitMap <- function(id=NULL, label=NULL, value=NULL, clickData=NULL, hoverNodeData=NULL) {
    
    props <- list(id=id, label=label, value=value, clickData=clickData, hoverNodeData=hoverNodeData)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'CircuitMap',
        namespace = 'circuit_graph',
        propNames = c('id', 'label', 'value', 'clickData', 'hoverNodeData'),
        package = 'circuitGraph'
        )

    structure(component, class = c('dash_component', 'list'))
}
