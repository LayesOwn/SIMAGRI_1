# -*- coding: utf-8 -*-
"""
SIMAGRI Sénégal - Point d'entrée de l'application
Version simplifiée pour le Sénégal uniquement
"""

from dash import html, dcc
from dash.dependencies import Input, Output

import os

from app import app
from app import server

from navbar import navbar

# Import des modules Sénégal (depuis apps/senegal/)
from apps.senegal import about
from apps.senegal import historical
from apps.senegal import forecast_FResampler as forecast

##########################################################################
# Configuration Sénégal
##########################################################################

APP_CONFIG = {
    "logo": app.get_asset_url("CWP_IRI_ISRA_senegal.GIF"),
    "tutorial": "https://sites.google.com/iri.columbia.edu/simagri-french/simagri-tutorial",
    "feedback": "https://sites.google.com/iri.columbia.edu/simagri-senegal/user-feedback-survey-form",
    "paths": {
        "/about": about.layout,
        "/historical": historical.layout,
        "/forecast": forecast.layout,
    },
}

##########################################################################
# Layout principal
##########################################################################

body = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
], id="body")

app.layout = html.Div([
    navbar(APP_CONFIG["logo"], "Senegal", APP_CONFIG["tutorial"], APP_CONFIG["feedback"]),
    body
])

##########################################################################
# Callback de navigation
##########################################################################

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
)
def display_page(pathname):
    """Affiche la page correspondant au chemin URL."""
    if pathname in APP_CONFIG["paths"]:
        return APP_CONFIG["paths"][pathname]
    
    # Page d'accueil par défaut (en français)
    return html.Div([
        html.H3("SIMAGRI - Sénégal"),
        html.P("Outil d'aide à la décision pour la modélisation climato-agricole."),
        html.P("Cliquez sur le menu pour accéder aux analyses."),
    ], className="text-center p-5")


##########################################################################
# Démarrage du serveur
##########################################################################

port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run_server(
        debug=False,
        host="0.0.0.0",
        port=port
    )
