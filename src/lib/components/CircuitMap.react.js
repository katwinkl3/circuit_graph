import React, {Component} from 'react';
import ReactDOM from 'react-dom'
import PropTypes from 'prop-types';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Row, Container, Col, Button, ButtonDropdown, DropdownMenu,
    DropdownToggle, DropdownItem, Card, CardText, CardBody, CardTitle, CardSubtitle} from 'reactstrap';
import Cytoscape from 'cytoscape';
import CytoscapeComponent from 'react-cytoscapejs';
import {scaleSequential} from 'd3-scale';
import {interpolateSpectral} from 'd3-scale-chromatic';
import {select, scaleLinear, axisBottom} from 'd3';
import popper from 'cytoscape-popper';
import KaTex from 'katex';

Cytoscape.use(popper);


/**
 * Assumes horizontal stack
 */
export default class CircuitMap extends Component {
    constructor(props) {
        super(props);
        this.ibm_qubits_pos = {
            15:{0:[0,0], 1:[50,0], '2':[100,0], '3':[150,0], '4':[200,0],'5':[250,0],'6':[300,0],
                '7':[350, 50], '8':[300,50],'9':[250,50],'10':[200,50],'11':[150,50],'12':[100,50],
                '13':[50,50],'14':[0,50]
            }
        }
        this.ibm_qubits_hover = {
            15:{0:'top', 1:'top', 2:'top', 3:'top', 4:'top', 5:'top', 6:'top', 7:'bottom',
                8:'bottom', 9:'bottom', 10:'bottom', 11:'bottom', 12:'bottom', 13:'bottom', 14:'bottom'}
        }

        // Set up default background color, readout error and its color
        this.backgroundColor = Array(this.props.value.num_qubits).fill("#808080")
        this.color_fn = scaleSequential(interpolateSpectral)

        this.readoutError = this.scaleError('readout_error')
        this.readoutErrorColor = []
        this.readoutError.map( (v, i) => {
            this.readoutErrorColor.push(this.color_fn(v/Math.max(...this.readoutError)))

        })


        let res = this.createErrorLists('T1')
        this.t1ErrorColor = res[1]
        this.t1Error = res[0]

        let elements = this.createElements(this.backgroundColor)
        this.state = {qubitInfo: false, elements: elements, errorList: [], mapTitle: "Display Error",
            focusQubit: this.props.value.selection}

        this.cyPopperRef = React.createRef()
        this.legend = React.createRef()


    }

    scaleError(info){
        let errors = []
        Object.keys(this.props.value.qubit_info).forEach(k => {
            errors.push(this.props.value.qubit_info[k][info][0])
        })
        return errors
    }

    // Helper to convert to RGB
    convertToHex (rgb){
        let res = "#"
        let val = rgb.slice(4, -1).split(",")
        val.forEach(v => {
            let hex = parseInt(v).toString(16).toUpperCase()
            if (hex.length < 2){
                res += '0'
            }
            res += hex
        })
        return res
    }

    createErrorLists(error_type){
        let errors = this.scaleError(error_type)
        let max = Math.max(...errors)
        let error_color = []
        errors.map( (v, i) => {
            error_color.push(this.color_fn(v/max))
        })
        return [errors, error_color]
    }

    createElements(colorArray){ //TODO: Separate Edges and Nodes generation for better runtime
        let nodes = []
        let edges = []
        let node_list = []
        let value = this.props.value
        value.edges.forEach( i => {
            i.forEach(v => {
                if (!node_list.includes(v)) {
                    node_list.push(v)
                    nodes.push({data: {id:v, label:'q'+v}, grabbable:false, selectable: false,
                        style: {'background-color': colorArray[v]},
                        position:{x:this.ibm_qubits_pos[value.num_qubits][v][0], y:this.ibm_qubits_pos[value.num_qubits][v][1]}})
                }
            })
            edges.push({data:{source:i[0], target:i[1]}})
        })
        return nodes.concat(edges)
    }

    createLegend(error_list){
        let axisScale = scaleLinear()
            .domain([Math.min(...error_list), Math.max(...error_list)])
            .range([0, 300])
        let axisBottomObj = g => g
            .attr("class", `x-axis`)
            .attr("transform", `translate(0,20)`)
            .call(axisBottom(axisScale)
                .ticks(300 / 50))
        return axisBottomObj
    }

    createPopUp(id){
            let div = document.createElement('div')
            ReactDOM.render(
                <p>{this.state.errorList[id]}</p>
                ,div)
            // div.innerHTML = 'Popper content';
            document.body.appendChild(div);
            return div
    }

    setUpListeners = () => {
        this.cy.on('click', 'node', (e) => {
            this.setState({focusQubit: e.target.id()})
        })
        this.cy.on('mouseover', 'node', (e) => {
            let idx = e.target.id()
            this.cyPopperRef.current = e.target.popper({
                content: this.createPopUp(idx),
                popper: {
                    placement: this.ibm_qubits_hover[this.props.value.num_qubits][idx],
                    removeOnDestroy: true,
                },
            })
        })

        this.cy.on('mouseout', 'node', (e) => {
            if (this.cyPopperRef) {
                this.cyPopperRef.current.destroy();
            }
        })
    }

    componentDidMount = () => {
        this.setUpListeners()

        let svg = select('#colorLegend')
        let defs = svg.append("defs")
        let linearGradient = defs.append("linearGradient")
            .attr("id", "linear-gradient")
        linearGradient
            .attr("x1", "0%")
            .attr("y1", "0%")
            .attr("x2", "100%")
            .attr("y2", "0%")
        linearGradient.selectAll("stop")
            .data([
                {offset: "0%", color: this.convertToHex(this.color_fn(0))},
                {offset: "10%", color: this.convertToHex(this.color_fn(0.1))},
                {offset: "20%", color: this.convertToHex(this.color_fn(0.2))},
                {offset: "30%", color: this.convertToHex(this.color_fn(0.3))},
                {offset: "40%", color: this.convertToHex(this.color_fn(0.4))},
                {offset: "50%", color: this.convertToHex(this.color_fn(0.5))},
                {offset: "60%", color: this.convertToHex(this.color_fn(0.6))},
                {offset: "70%", color: this.convertToHex(this.color_fn(0.7))},
                {offset: "80%", color: this.convertToHex(this.color_fn(0.8))},
                {offset: "90%", color: this.convertToHex(this.color_fn(0.9))},
                {offset: "100%", color: this.convertToHex(this.color_fn(1))}
            ])
            .enter().append("stop")
            .attr("offset", function(d) { return d.offset; })
            .attr("stop-color", function(d) { return d.color; })
        svg.append("rect")
            .attr("width", 300)
            .attr("height", 20)
            .style("fill", "url(#linear-gradient)")
        svg.append('g')
            .call(this.createLegend(this.state.errorList))

        this.legend.current = svg

    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.value.selection != prevProps.value.selection){
            if (this.props.value.selection > 0){ //TODO: 1)Modify so clicking on button resets selection 2) change to state not props
                console.log("CHANGED to ")
                console.log(this.props.value.selection)
                this.backgroundColor.forEach((v, idx) => {
                    this.cy.$id(idx).style('background-color', v)
                })
                this.cy.$id(0).style('background-color', "red")
                this.cy.$id(1).style('background-color', "red")
                this.cy.$id(2).style('background-color', "red")
            }


        }
    }

    render() {
        const {id, label, setProps, value} = this.props;

        // Latex
        let latex = document.createElement('div')
        let latex_container = document.createElement('div')
        KaTex.render("c = \\pm\\sqrt{a^2 + b^2}", latex, {throwOnError:false})

        return (
            <div id={id}>
                <div>
                    <div>
                        <ButtonDropdown isOpen={this.state.qubitInfo} toggle={()=>{
                            this.setState(prevState => ({...prevState, qubitInfo: !prevState.qubitInfo}))
                        }}>
                            <DropdownToggle caret>
                                {this.state.mapTitle}
                            </DropdownToggle>
                            <DropdownMenu>
                                <DropdownItem
                                    onClick={ () => {
                                        this.setState({errorList: this.readoutError, mapTitle: "Readout Error"})
                                        this.readoutErrorColor.forEach((v, idx) => {
                                            this.cy.$id(idx).style('background-color', v)
                                        })
                                        select("g").remove()
                                        this.legend.current.append('g')
                                            .call(this.createLegend(this.state.errorList))
                                        this.legend.current.attr("id","axis_plot")
                                    }}
                                >Readout Error</DropdownItem>
                                <DropdownItem
                                    onClick={ () => {
                                        this.setState({errorList: this.t1Error, mapTitle: "T1 Error"})
                                        this.t1ErrorColor.forEach((v, idx) => {
                                            this.cy.$id(idx).style('background-color', v)
                                        })
                                        // this.legend.current = this.legend_reset
                                        select("g").remove()
                                        this.legend.current.append('g')
                                            .call(this.createLegend(this.state.errorList))
                                        this.legend.current.attr("id","axis_plot")
                                    }}
                                >T1 Error</DropdownItem>
                                <DropdownItem
                                    onClick={() => {
                                        this.setState({errorList: [], mapTitle: "Error Display"})
                                        this.backgroundColor.forEach((v, idx) => {
                                            this.cy.$id(idx).style('background-color', v)
                                        })
                                        // this.legend.current = this.legend_reset
                                        select("g").remove()
                                    }}
                                >Default</DropdownItem>
                            </DropdownMenu>
                        </ButtonDropdown>
                    </div>
                </div>
                <Row>
                    <Col>
                        <CytoscapeComponent
                            cy={(cy) => {this.cy = cy}}
                            elements={[...this.state.elements]}
                            style={ { width: '600px', height: '200px' } }
                        />
                        <svg id="colorLegend"></svg>
                    </Col>
                    <Col>
                        <Card>
                            <CardBody>
                                <CardTitle tag="h5">Qubit Information</CardTitle>
                                <CardSubtitle tag="h7">{"Readout Error: "+this.readoutError[this.state.focusQubit]+"\n"}</CardSubtitle>
                                <CardSubtitle tag="h7">{"T1 Error: "+this.t1Error[this.state.focusQubit]+"\n"}</CardSubtitle>
                                <CardSubtitle tag="h7">{"Others: ..."}</CardSubtitle>
                                <CardText tag="h7">{"H gate: ..."}</CardText>
                            </CardBody>
                        </Card>
                    </Col>
                </Row>

                <div ref={(latex) => {latex && latex.appendChild(latex_container)}}/>


            </div>
        )
    }
}

CircuitMap.defaultProps = {
    clickData: null
};

CircuitMap.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * A label that will be printed when this component is rendered.
     */
    label: PropTypes.string.isRequired,

    /**
     * The value displayed in the input.
     */
    value: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func,

    /**
     * Data from latest click event. Read-only.
     */
    clickData: PropTypes.object,

    /**
     * Data of hovered node
     */
    hoverNodeData: PropTypes.object
};
