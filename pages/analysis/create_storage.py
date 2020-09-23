import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output


def create_storage_div(analysis_pages):
    storage = []
    for page in analysis_pages:
        for stored_metric in page.page.storage:
            storage.append(dcc.Store(id=construct_store_div_name(page, stored_metric), storage_type='session'))

    return html.Div(storage)


def create_output_list(analysis_pages):
    outputs = []
    for page in analysis_pages:
        for metric in page.page.storage:
            outputs.append(Output(construct_store_div_name(page, metric), 'data'))

    return outputs


def construct_store_div_name(page, stored_metric):
    return '-'.join((page.page.id, stored_metric))
