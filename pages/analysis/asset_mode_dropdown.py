import dash_core_components as dcc
import dash_html_components as html


def generate_analysis_mode_dropdown(asset_list):
    asset_modes = [{'label': asset_name, 'value': asset_name} for asset_name in asset_list]

    analysis_mode_dropdown = html.Div(
        [
            dcc.Markdown('''> #### By Asset:''', style={'margin-top': '16px'}),
            dcc.Dropdown(id='asset_modes', options=asset_modes, value='By Asset', className='dropdown2'),
        ],
        style={'display': 'flex', 'flexWrap': 'wrap'}
    )
    return analysis_mode_dropdown
