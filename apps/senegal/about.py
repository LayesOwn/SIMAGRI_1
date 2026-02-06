# -*- coding: utf-8 -*-
"""
SIMAGRI Sénégal - Page À propos
"""

from dash import html
import dash_bootstrap_components as dbc


layout = html.Div(
    dbc.Row(
        dbc.Col(
            [
                html.Br(),
                
                # Titre anglais
                html.H4(
                    "Climate-Agriculture Modeling Decision Support Tool, SIMAGRI-Senegal",
                    className="text-primary"
                ),
                
                # Titre français
                html.H4(
                    "Outil d'aide à la décision pour la modélisation climato-agricole, SIMAGRI-Sénégal",
                    className="text-success"
                ),
                
                html.Hr(),
                
                # Description anglais
                html.Div(
                    [
                        html.P(
                            """
                            Smart planning of annual crop production requires consideration of possible scenarios.
                            The SIMAGRI tool adopts crop simulation models included in the DSSAT package 
                            (Decision Support System for Agrotechnology Transfer).
                            """
                        ),
                        html.P(
                            """
                            The methodology was developed by the IRI (International Research Institute for 
                            Climate and Society / Columbia University) in collaboration with ISRA 
                            (Institut Sénégalais de Recherches Agricoles).
                            """
                        ),
                        html.P(
                            """
                            The purpose of this tool is to support decision-making of the producer or 
                            technical advisor, which facilitates discussion of optimal production strategies, 
                            risks of technology adoption, and evaluation of long-term effects, 
                            considering interactions of various factors.
                            """
                        ),
                    ],
                    className="mb-4"
                ),
                
                # Description français
                html.Div(
                    [
                        html.P(
                            """
                            La planification intelligente de la production de cultures annuelles nécessite 
                            la prise en compte de scénarios possibles. L'outil SIMAGRI adopte des modèles 
                            de simulation de cultures inclus dans le package DSSAT 
                            (Decision Support System for Agrotechnology Transfer).
                            """
                        ),
                        html.P(
                            """
                            La méthodologie a été développée par l'IRI (International Research Institute 
                            for Climate and Society / Columbia University) en collaboration avec 
                            l'Institut Sénégalais de Recherches Agricoles (ISRA), Sénégal.
                            """
                        ),
                        html.P(
                            """
                            L'objectif de cet outil est de soutenir la prise de décision du producteur 
                            ou du conseiller technique, ce qui facilite la discussion sur les stratégies 
                            de production optimales, les risques liés à l'adoption de la technologie 
                            et l'évaluation des effets à long terme, en tenant compte des interactions 
                            de divers facteurs.
                            """
                        ),
                    ],
                    className="mb-4"
                ),
                
                html.Hr(),
                
                # Crédits
                html.Div(
                    [
                        html.H5("Crédits / Credits:", className="text-muted"),
                        html.Ul(
                            [
                                html.Li("Eunjin Han, Ph.D. - IRI"),
                                html.Li("Walter Baethgen, Ph.D. - IRI"),
                                html.Li("James Hansen, Ph.D. - IRI"),
                                html.Li("Kesha Kumshayev - IRI"),
                                html.Li("Adama Faye - Institut Sénégalais de Recherches Agricoles (ISRA)"),
                                html.Li("Mbaye Diop - Institut Sénégalais de Recherches Agricoles (ISRA)"),
                                html.Li("Abdoulaye Diop - Institut Sénégalais de Recherches Agricoles (ISRA)"),
                            ]
                        ),
                    ]
                ),
            ],
            className="text-center p-4"
        )
    )
)
