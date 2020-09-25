import dash_core_components as dcc
import dash_html_components as html


def generate_analysis_mode_dropdown(page_name):

    analysis_mode_dropdown = html.Div(
        [
            dcc.Markdown('''> #### Asset:''', style={'margin-top': '16px'}),
            dcc.Dropdown(id='-'.join((page_name, 'asset-dropdown')), className='dropdown2'),
        ],
        style={'display': 'flex', 'flexWrap': 'wrap'}
    )
    return analysis_mode_dropdown
