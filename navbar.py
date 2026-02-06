# -*- coding: utf-8 -*-
"""
SIMAGRI Sénégal - Barre de navigation
Version simplifiée pour le Sénégal uniquement
"""

from dash import html
import dash_bootstrap_components as dbc


def navbar(logo, country, tutorial, feedback):
    """
    Crée la barre de navigation pour SIMAGRI Sénégal.
    
    Args:
        logo: URL du logo
        country: Nom du pays (ignoré, toujours Sénégal)
        tutorial: URL du tutoriel
        feedback: URL du formulaire de retour
    
    Returns:
        dbc.Navbar: Composant barre de navigation
    """
    
    # Liens du menu (en français)
    tutorial_link = dbc.NavItem(
        dbc.NavLink("Manuel", target="_blank", href=tutorial)
    )
    feedback_link = dbc.NavItem(
        dbc.NavLink("Retour d'information", target="_blank", href=feedback)
    )
    
    # Construction de la navbar
    nav = dbc.Navbar(
        [
            # LOGO & MARQUE
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=logo, height="50px")),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "SIMAGRI-Sénégal",
                                className="ml-3 font-weight-bold"
                            ),
                            className="my-auto"
                        ),
                    ],
                    align="center",
                    className="g-0",  # Remplace no_gutters (déprécié)
                ),
                href="/about",
            ),
            
            # LIENS DE NAVIGATION
            dbc.Nav(
                [
                    dbc.NavItem(
                        dbc.NavLink("Analyse historique", href="/historical")
                    ),
                    dbc.NavItem(
                        dbc.NavLink("Analyse des prévisions", href="/forecast")
                    ),
                    tutorial_link,
                    feedback_link,
                ],
                navbar=True,
            ),
        ],
        color="white",
        dark=False,
        className="mb-2",
    )
    
    return nav
