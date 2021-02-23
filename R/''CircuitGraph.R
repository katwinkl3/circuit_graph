# AUTO GENERATED FILE - DO NOT EDIT

''CircuitGraph <- function(id=NULL, label=NULL, value=NULL, clickData=NULL) {
    
    props <- list(id=id, label=label, value=value, clickData=clickData)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'CircuitGraph',
        namespace = 'circuit_graph',
        propNames = c('id', 'label', 'value', 'clickData'),
        package = 'circuitGraph'
        )

    structure(component, class = c('dash_component', 'list'))
}
