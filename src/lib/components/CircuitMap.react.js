import React, {Component} from 'react';
import PropTypes from 'prop-types';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Row, Container, Col, Button} from 'reactstrap';
import CytoscapeComponent from 'react-cytoscapejs';
import {scaleSequential} from 'd3-scale';
import {interpolateSpectral} from 'd3-scale-chromatic';

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

        // Set up default background color, readout error and its color
        this.backgroundColor = Array(this.props.value.num_qubits).fill("#808080")
        // for (const x of Array(this.props.value.num_qubits).keys()) {
        //     this.backgroundColor[x] = "#808080"
        // }
        this.color_fn = scaleSequential(interpolateSpectral)
        this.readoutError = this.scaleError('readout_error')
        this.readoutErrorColor = []
        this.readoutError.map( (v, i) => {
            this.readoutErrorColor.push(this.color_fn(v/Math.max(...this.readoutError)))

        })

        let elements = this.createElements(this.backgroundColor)
        this.state = {qubitInfo: true, elements: elements}

        this.t1Error = this.scaleError('T1')

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

    toggleQubitInfo(){
        let value = this.props.value.qubit_info
    }

    // handleCy(cy){
    //     this._cy = cy
    // }

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

    setUpListeners = () => {
        this.cy.on('click', 'node', (event) => {
            console.log(event.target)
        })
    }

    componentDidMount = () => {
        this.setUpListeners()
    }


    render() {
        const {id, label, setProps, value} = this.props;

        // let nodes = []
        // let edges = []
        // let node_list = []
        // value.edges.forEach( i => {
        //     let s = i[0];
        //     let e = i[1]
        //     console.log("Im re-rendering "+this.state[s]+this.state[e])
        //     if (!node_list.includes(s)) {
        //         node_list.push(s)
        //         nodes.push({data: {id:s, label:'q'+s}, grabbable:false, selectable: false,
        //             style: {'background-color': this.state[s]},
        //             // style: {'background-color': this.state.backgroundColor[s]},
        //             position:{x:this.ibm_qubits_pos[value.num_qubits][s][0], y:this.ibm_qubits_pos[value.num_qubits][s][1]}})
        //     }
        //     if (!node_list.includes(e)) {
        //         node_list.push(e)
        //         nodes.push({data: {id:e, label:'q'+e}, grabbable:false, selectable: false,
        //             style: {'background-color': this.state[e]},
        //             // style: {'background-color': this.state.backgroundColor[e]},
        //             position:{x:this.ibm_qubits_pos[value.num_qubits][e][0], y:this.ibm_qubits_pos[value.num_qubits][e][1]}})
        //     }
        //     edges.push({data:{source:s, target:e}})
        // })

        return (
            <div id={id}>
                <div>
                    <Button onClick={() => {

                        if (this.state.qubitInfo){
                            this.readoutErrorColor.forEach((v,idx) => {
                                this.cy.$id(idx).style('background-color', v)
                            })
                            // this.setState(prevState => ({...prevState,
                            //     elements: this.createElements(this.readoutErrorColor),
                            //     qubitInfo: !prevState.qubitInfo})
                            // )
                            // this.setState(prevState => ({...prevState, ...this.readoutErrorColor, qubitInfo: !prevState.qubitInfo}))
                        } else {
                            this.backgroundColor.forEach((v,idx) => {
                                this.cy.$id(idx).style('background-color', v)
                            })
                        }
                        this.setState(prevState => ({...prevState, qubitInfo: !prevState.qubitInfo}))
                    }}>
                        Show
                    </Button>
                </div>
                <CytoscapeComponent
                    cy={(cy) => {this.cy = cy}}
                    elements={[...this.state.elements]}
                    // elements={nodes.concat(edges)}
                    style={ { width: '600px', height: '600px' } }
                />
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
