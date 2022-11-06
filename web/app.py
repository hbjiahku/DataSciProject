from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc
from config.config_helper import get_config, NETWORK_CFG

external_stylesheets = [dbc.themes.SLATE]
app = Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Automatic Investment System'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

    dash.page_container
])

if __name__ == '__main__':
    network_config = get_config(NETWORK_CFG)
    app.run_server(debug=True, host=network_config['host'], port=network_config['ui_port'], dev_tools_hot_reload=True)