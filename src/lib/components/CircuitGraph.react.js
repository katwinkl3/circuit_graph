import React, {Component} from 'react';
import PropTypes from 'prop-types';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Row, Container, Col} from 'reactstrap';

/**
 * Assumes horizontal stack
 */
export default class CircuitGraph extends Component {
    constructor(props) {
        super(props);
        let circ_state = {}
        Object.keys(this.props.value.circuit_drawing).map(k => {
            circ_state[k] = true
        })
        this.state = {...circ_state, prevButton:'', gate: 0}
    }

    render() {
        const {id, label, setProps, value} = this.props;
        const qubits = [...Array(value.width).keys()]


        return (
            <div id={id}>
                <Container>
                    <Row>
                        <Col style={{sm:1}}>
                            {qubits.map(val => {
                                return <Row><button
                                    style={{width:'30px', height:'30px', fontSize:'16px', marginLeft: '135px', marginTop:'10px'}}
                                    id={val}
                                    className={"buttons"}
                                    onClick={() => {
                                        console.log(this.state.prevButton)
                                        this.props.setProps({clickData: {pointValue: val}});
                                        if (this.state.prevButton != ''){
                                            document.getElementById(this.state.prevButton).style.backgroundColor = "#F2F2F2"
                                        }
                                        document.getElementById(val).style.backgroundColor = "#FAE3A3"
                                        this.setState({prevButton: val})
                                    }}
                                >
                                    {"Q"+val}
                                </button></Row>
                                }
                            )}
                        </Col>
                        <Row style={{paddingRight: '10px'}}>
                            {Object.keys(value.circuit_drawing).map((k, idx) => {
                                return <div><pre
                                    style={{lineHeight: '20px', overflowY:'hidden',
                                        margin: '0px 0px 0px 0px', padding: '0px 0px 0px'}}
                                    onClick={() => {

                                        this.props.setProps({mapData: idx})
                                        // this.props.setProps({mapData: this.state.gate})
                                        // this.setState(prevState => {gate: prevState.gate + 1})
                                    }}
                                    //{value.circuit_drawing[k][this.state.k]}
                                >{value.circuit_drawing[k][this.state[k]? 0: 1]}</pre>
                                <button onClick={() => {
                                    const update = {}
                                    update[k] = !this.state[k] //TODO: Not using prevState because yolo (idk how help)
                                    this.setState(update)
                                }}>Expand</button>
                                </div>
                            })}
                        </Row>
                    </Row>
                </Container>
            </div>
        );
    }
}

CircuitGraph.defaultProps = {
    clickData: null,
    mapData: null
};

CircuitGraph.propTypes = {
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
     * Data from latest click event. Read-only.
     */
    mapData: PropTypes.number
};
