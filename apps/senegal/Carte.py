import dash
import dash_html_components as html
import dash_leaflet as dl

# Les positions des villes
Position = {
    "Dakar": [14.700047543225823, -17.50001290971342],
    "Bambey": [15.000134707867867, -16.49997854796095],
    "Mbacke": [14.80013483323102, -15.900042920979626],
    "Fatick_Niakhar": [14.500155792376464, -16.400032192151638],
    "Foundiougne": [13.90012496236718, -16.400010734495066],
    "Birkilane": [14.10010404228193, -15.800000005654653],
    "Kounguel": [14.00014572838203, -14.80002146332832],
    "Kaolack": [14.100156070240521, -16.10000000565467],
    "Nioro du Rip": [13.700156340499975, -15.800032192171074],
    "Kolda": [12.800198769551196, -14.60000000568494],
    "Medina Yoroufoula": [13.100156731601537, -14.600032192184925],
    "Velingrara": [12.90017777424403, -14.100000005682656],
    "Linguere": [15.300155213889152, -15.500042920966724],
    "Louga": [15.500103371403704, -16.0000214632902],
    "Saint Louis": [16.100133989082607, -16.49997854793152],
    "Sedhiou": [12.700198848162987, -15.6000429210294],
    "Koumpentoum": [14.00017695879087, -14.600032192163923],
    "Tambacounda 1": [13.100177630843898, -13.300021463349408],
    "Tambacounda 2": [13.800177111914401, -13.700010734497527],
    "Tambacounda 3": [13.90015620632161, -14.100042921001881],
    "Mbour": [14.40019742960074, -17.00000000564732],
    "Thies": [14.800186697639713, -17.000000005637286],
    "Tivaoune": [15.000196887377449, -16.800021463303363],
    "Bignona": [13.000188156663333, -16.200010734516013],
    "Oussouye": [12.50016758003306, -16.499989276855867],
    "Ziguinchor": [12.500157105519985, -16.00004292103381],
}

# Créer l'application Dash
app = dash.Dash(__name__)

# Créer les marqueurs pour chaque position
markers = [dl.Marker(position=coords, children=dl.Tooltip(ville)) for ville, coords in Position.items()]

# Layout de l'application
app.layout = html.Div([
    html.H1("Carte"),
    dl.Map(center=(14.10010404228193, -15.800000005654653), zoom=7, children=[
        dl.TileLayer(),
        dl.LayerGroup(markers)
    ], style={'width': '100%', 'height': '500px'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
