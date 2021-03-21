import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, BasicAer, IBMQ, execute, transpile
from qiskit.quantum_info.states import DensityMatrix
from qiskit.quantum_info.operators import PauliTable
from qiskit.visualization import plot_histogram, plot_bloch_vector, plot_circuit_layout
from qiskit.providers.ibmq import least_busy
from qiskit.test.mock import FakeBoeblingen
from math import gcd
from numpy.random import randint
from fractions import Fraction
import math
import io
from PIL import Image
from dash.dependencies import Input, Output, State
import json
import re
from circuit_graph import CircuitGraph, CircuitMap
import datetime

def tzlocal():
    return 0

num_qubits = 15
config = [[0, 1], [0, 14], [1, 0], [1, 2], [1, 13], [2, 1], [2, 3], [2, 12], [3, 2], [3, 4], [3, 11], [4, 3], [4, 5], [4, 10], [5, 4], [5, 6], [5, 9], [6, 5], [6, 8], [7, 8], [8, 6], [8, 7], [8
, 9], [9, 5], [9, 8], [9, 10], [10, 4], [10, 9], [10, 11], [11, 3], [11, 10], [11, 12], [12, 2], [12, 11], [12, 13], [13, 1], [13, 12], [13, 14], [14, 0], [14, 13]]
b = '''{0: {'T1': (5.8987897288593676e-05, datetime.datetime(2021, 3, 19, 14, 11, 10, tzinfo=tzlocal())), 'T2': (9.211643444265062e-05, datetime.datetime(2021, 3, 19, 14, 12, 30, tzinfo=tzloc
al())), 'frequency': (5114620288.937647, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'anharmonicity': (0.0, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal
())), 'readout_error': (0.027900000000000036, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas0_prep1': (0.0474, datetime.datetime(2021, 3, 19, 14, 10, 22, tzi
nfo=tzlocal())), 'prob_meas1_prep0': (0.0084, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'readout_length': (3.555555555555555e-06, datetime.datetime(2021, 3, 19, 14
, 10, 22, tzinfo=tzlocal()))}, 1: {'T1': (4.4546849476500186e-05, datetime.datetime(2021, 3, 19, 14, 11, 10, tzinfo=tzlocal())), 'T2': (4.799893564791908e-05, datetime.datetime(2021, 3
, 19, 14, 16, 58, tzinfo=tzlocal())), 'frequency': (5235044046.175993, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'anharmonicity': (0.0, datetime.datetime(2021, 3,
19, 19, 35, 12, tzinfo=tzlocal())), 'readout_error': (0.047699999999999965, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas0_prep1': (0.075, datetime.datetime
(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas1_prep0': (0.020399999999999974, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'readout_length': (3.55555555555
5555e-06, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal()))}, 2: {'T1': (6.286211958434261e-05, datetime.datetime(2021, 3, 19, 14, 11, 10, tzinfo=tzlocal())), 'T2': (8.9163
68786981119e-05, datetime.datetime(2021, 3, 19, 14, 12, 30, tzinfo=tzlocal())), 'frequency': (5038351629.985002, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'anharmo
nicity': (0.0, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'readout_error': (0.03600000000000003, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'pro
b_meas0_prep1': (0.0594, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas1_prep0': (0.012599999999999945, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzl
ocal())), 'readout_length': (3.555555555555555e-06, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal()))}, 3: {'T1': (5.405921995320968e-05, datetime.datetime(2021, 3, 19, 14,
 11, 10, tzinfo=tzlocal())), 'T2': (1.79257557811491e-05, datetime.datetime(2021, 3, 19, 14, 16, 58, tzinfo=tzlocal())), 'frequency': (4894442502.208525, datetime.datetime(2021, 3, 19,
 19, 35, 12, tzinfo=tzlocal())), 'anharmonicity': (0.0, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'readout_error': (0.05180000000000007, datetime.datetime(2021, 3,
 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas0_prep1': (0.07479999999999998, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas1_prep0': (0.0288, datetime.date
time(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'readout_length': (3.555555555555555e-06, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal()))}, 4: {'T1': (5.572524669549611
e-05, datetime.datetime(2021, 3, 19, 14, 11, 10, tzinfo=tzlocal())), 'T2': (6.619449371731735e-05, datetime.datetime(2021, 3, 19, 14, 12, 30, tzinfo=tzlocal())), 'frequency': (50220299
46.793027, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'anharmonicity': (0.0, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'readout_error': (0.0476
99999999999965, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas0_prep1': (0.07579999999999998, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())),
'prob_meas1_prep0': (0.0196, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'readout_length': (3.555555555555555e-06, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=
tzlocal()))}, 5: {'T1': (1.5131951779189434e-05, datetime.datetime(2021, 3, 17, 13, 58, 19, tzinfo=tzlocal())), 'T2': (2.367854812074798e-05, datetime.datetime(2021, 3, 19, 14, 16, 58,
 tzinfo=tzlocal())), 'frequency': (5073154532.635169, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'anharmonicity': (0.0, datetime.datetime(2021, 3, 19, 19, 35, 12, t
zinfo=tzlocal())), 'readout_error': (0.04800000000000004, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas0_prep1': (0.0806, datetime.datetime(2021, 3, 19, 14,
 10, 22, tzinfo=tzlocal())), 'prob_meas1_prep0': (0.01539999999999997, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'readout_length': (3.555555555555555e-06, datetime
.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal()))}, 6: {'T1': (5.503698477544899e-05, datetime.datetime(2021, 3, 19, 14, 11, 10, tzinfo=tzlocal())), 'T2': (7.24703242528632e-05, da
tetime.datetime(2021, 3, 19, 14, 12, 30, tzinfo=tzlocal())), 'frequency': (4929463885.243281, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'anharmonicity': (0.0, date
time.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'readout_error': (0.20240000000000002, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas0_prep1': (0.
056, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas1_prep0': (0.3488, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'readout_length': (3.555
555555555555e-06, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal()))}, 7: {'T1': (3.722308559941505e-05, datetime.datetime(2021, 3, 19, 14, 11, 10, tzinfo=tzlocal())), 'T2':
 (2.1117938168646527e-05, datetime.datetime(2021, 3, 19, 14, 12, 30, tzinfo=tzlocal())), 'frequency': (4983244266.452782, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())),
 'anharmonicity': (0.0, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'readout_error': (0.0351999999999999, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal()
)), 'prob_meas0_prep1': (0.05279999999999996, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas1_prep0': (0.0176, datetime.datetime(2021, 3, 19, 14, 10, 22, tzi
nfo=tzlocal())), 'readout_length': (3.555555555555555e-06, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal()))}, 8: {'T1': (0.0001241825373491501, datetime.datetime(2021, 3,
18, 14, 2, 23, tzinfo=tzlocal())), 'T2': (5.614328085160751e-05, datetime.datetime(2021, 3, 19, 14, 16, 58, tzinfo=tzlocal())), 'frequency': (4751446120.384807, datetime.datetime(2021,
 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'anharmonicity': (0.0, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'readout_error': (0.024399999999999977, datetime.datetime(
2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas0_prep1': (0.0348, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas1_prep0': (0.014000000000000012, date
time.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'readout_length': (3.555555555555555e-06, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal()))}, 9: {'T1': (4.724454
350354599e-05, datetime.datetime(2021, 3, 19, 14, 11, 10, tzinfo=tzlocal())), 'T2': (6.815823216174609e-05, datetime.datetime(2021, 3, 18, 14, 4, 19, tzinfo=tzlocal())), 'frequency': (
4973518716.591253, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'anharmonicity': (0.0, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'readout_error':
 (0.040899999999999936, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas0_prep1': (0.0736, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob
_meas1_prep0': (0.0082, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'readout_length': (3.555555555555555e-06, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzloc
al()))}, 10: {'T1': (6.870419395334443e-05, datetime.datetime(2021, 3, 19, 14, 11, 10, tzinfo=tzlocal())), 'T2': (5.936113392936628e-05, datetime.datetime(2021, 3, 19, 14, 16, 58, tzin
fo=tzlocal())), 'frequency': (4944696803.632068, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'anharmonicity': (0.0, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo
=tzlocal())), 'readout_error': (0.05269999999999997, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas0_prep1': (0.08899999999999997, datetime.datetime(2021, 3,
 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas1_prep0': (0.0164, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'readout_length': (3.555555555555555e-06, datetime.date
time(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal()))}, 11: {'T1': (5.011265705810803e-05, datetime.datetime(2021, 3, 13, 14, 52, 55, tzinfo=tzlocal())), 'T2': (8.169556429937011e-05, datet
ime.datetime(2021, 3, 19, 14, 12, 30, tzinfo=tzlocal())), 'frequency': (4997447270.8771925, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'anharmonicity': (0.0, dateti
me.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'readout_error': (0.04510000000000003, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas0_prep1': (0.08
040000000000003, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas1_prep0': (0.0098, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'readout_len
gth': (3.555555555555555e-06, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal()))}, 12: {'T1': (8.086774473779273e-05, datetime.datetime(2021, 3, 19, 14, 11, 10, tzinfo=tzloc
al())), 'T2': (8.172892782273958e-05, datetime.datetime(2021, 3, 19, 14, 16, 58, tzinfo=tzlocal())), 'frequency': (4763629510.827328, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=
tzlocal())), 'anharmonicity': (0.0, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'readout_error': (0.028100000000000014, datetime.datetime(2021, 3, 19, 14, 10, 22, tz
info=tzlocal())), 'prob_meas0_prep1': (0.042200000000000015, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas1_prep0': (0.014, datetime.datetime(2021, 3, 19, 1
4, 10, 22, tzinfo=tzlocal())), 'readout_length': (3.555555555555555e-06, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal()))}, 13: {'T1': (2.6220304744428412e-05, datetime.da
tetime(2021, 3, 19, 14, 11, 10, tzinfo=tzlocal())), 'T2': (2.7878752035367712e-05, datetime.datetime(2021, 3, 19, 14, 12, 30, tzinfo=tzlocal())), 'frequency': (4973580477.119138, datet
ime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'anharmonicity': (0.0, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'readout_error': (0.06130000000000002, d
atetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas0_prep1': (0.0926, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas1_prep0': (0.0300000
00000000027, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'readout_length': (3.555555555555555e-06, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal()))}, 14
: {'T1': (4.5331602739109366e-05, datetime.datetime(2021, 3, 18, 14, 2, 23, tzinfo=tzlocal())), 'T2': (2.6957904090441556e-05, datetime.datetime(2021, 3, 19, 14, 16, 58, tzinfo=tzlocal
())), 'frequency': (5007395011.301539, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal())), 'anharmonicity': (0.0, datetime.datetime(2021, 3, 19, 19, 35, 12, tzinfo=tzlocal()
)), 'readout_error': (0.08099999999999996, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'prob_meas0_prep1': (0.13039999999999996, datetime.datetime(2021, 3, 19, 14, 1
0, 22, tzinfo=tzlocal())), 'prob_meas1_prep0': (0.0316, datetime.datetime(2021, 3, 19, 14, 10, 22, tzinfo=tzlocal())), 'readout_length': (3.555555555555555e-06, datetime.datetime(2021,
 3, 19, 14, 10, 22, tzinfo=tzlocal()))}}
'''

res = ''
for i in b.split('\n'):
    res += i
def tzlocal():
    return None
qubit_info = eval(res)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        # Title #



        html.Div([
            html.Div([
                html.Div([
                    html.P("Circuit Operations", style={"text-align": 'center'}),
                    # dcc.Graph(
                    #     id='q-circuit',
                    #     figure=fig3
                    # )

                ], style= {
                    'border-radius': '5px',
                    'background-color':  '#f9f9f9', 'margin': '5px', 'padding': '15px',
                    'position': 'relative', 'box-shadow': '2px 2px 2px lightgrey'
                }),
                html.Div([
                    html.P("Circuit Mapping", style={"text-align": 'center'}),
                    # html.Img(id='q-mapping',style={'right-margin':'5px', 'height':'80%', 'width':'80%'}),
                    CircuitMap(
                        id='q-map',
                        value={'num_qubits': num_qubits, 'edges': config, 'qubit_info':qubit_info},
                        label='label'
                    ),
                    # cyto.Cytoscape(
                    #     id='q-mapping',
                    #     elements=[]
                    # )
                ], style= {
                    'border-radius': '5px',
                    'background-color':  '#f9f9f9', 'margin': '1px', 'padding': '15px',
                    'position': 'relative', 'box-shadow': '2px 2px 2px lightgrey'
                })
            ], style={'width':'50%', 'position': 'relative'#'absolute', 'top': '30%', 'left':'10%', 'height':'400px'
                }),


        ], style={'display': 'flex'}),


        html.P("Sample of Summarized Circuit"),
        html.Button("Temp",id='button-1',style={'width':'10%'}),
        html.Img(id='img',src=app.get_asset_url('main_circ.png'), style={'height':'50%', 'width':'50%', 'margins':'10px'})
    ], style={'background-color': '#f2f2f2', "display": "flex", "flex-direction": "column",
              'font-size': '1.5em', 'line-height': '1.6', 'font-weight': '400',
              'font-family': "Arial", 'color': 'rgb(50, 50, 50)'}
)



# @app.callback(
#     Output('q-state', 'figure'),
#     [Input('q-circuit', 'clickData'), Input('state-count', 'value')])
# def display_click_data(clickData, value):
#     return create_state_plot(clickData, value)


# @app.callback(
#     Output('q-mapping', 'src'),
#     Input('q-test', 'mapData'))
# def update_output(value):
#     if str(value) == '0':
#         return app.get_asset_url('error_5.png')
#     if str(value) == '1':
#         return app.get_asset_url('error_1.png')
#     else:
#         return app.get_asset_url('error_9.png')

# @app.callback(
#     Output('q-map-noise', 'src'),
#     Input('q-test', 'clickData'))
# def update_output(clickData):
#     value = 0
#     if value == '0':
#         return app.get_asset_url('noise1.png')
#     if value == '1':
#         return app.get_asset_url('noise2.png')
#     else:
#         return app.get_asset_url('noise3.png')

if __name__ == '__main__':
    app.run_server(debug=True)
