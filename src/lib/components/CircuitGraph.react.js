import React, {Component} from 'react';
import PropTypes from 'prop-types';

/**
 * ExampleComponent is an example component.
 * It takes a property, `label`, and
 * displays it.
 * It renders an input with the property `value`
 * which is editable by the user.
 */
export default class CircuitGraph extends Component {
    render() {
        const {id, label, setProps, value} = this.props;
        const qubits = [...Array(value.width).keys()]


        return (
            <div id={id}>
                <div style={{display:'inline-flex'}}>
                    <div style={{display:'block'}}>
                        {qubits.map(val => {
                            return <button
                                style={{verticalAlign:'middle'}}
                                id={val}
                                onClick={() => {
                                    this.props.setProps({clickData: {pointValue: val}}); //TODO: Fix this
                                }}
                            >
                                {"Q"+val}
                            </button>
                            }
                        )}
                    </div>

                    <div>
                        <pre style={{lineHeight: '20px'}}>{value.circuit_data}</pre>
                    </div>
                </div>



            </div>
        );
    }
}

CircuitGraph.defaultProps = {
    clickData: null
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
    clickData: PropTypes.object
};
