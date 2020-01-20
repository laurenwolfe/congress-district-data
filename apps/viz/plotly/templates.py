import plotly.graph_objects as go


def style_grouped_bar():
    grouped_bar_template = go.layout.Template(
        layout=go.Layout(
            title=dict(
            ),
            xaxis=dict(
                title=dict(
                    font=dict(
                        family="Verdana",
                        size=16,
                        color='rgb(50,58,83)',
                    ),
                ),
                showgrid=True,
                gridwidth=1,
                gridcolor='rgb(210,210,210)',
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='rgb(220,220,220)',
                ticks="outside",
                tick0=-50,
                dtick=10,
                tickcolor='rgb(19,38,57)',
                visible=True,
            ),
            yaxis=dict(
                title=dict(
                    font=dict(
                        family="Helvetica",
                        size=16,
                        color='rgb(50,58,83)',
                    ),
                ),
                showgrid=True,
                gridwidth=1,
                gridcolor='rgb(210,210,210)',
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='rgb(220,220,220)',
                ticks="outside",
                tick0=0,
                dtick=10,
                tickcolor='rgb(19,38,57)',
                visible=True,
            ),
        )
    )
    return grouped_bar_template


def style_scatterplot():
    scatter_template = go.layout.Template(
        layout=go.Layout(
            plot_bgcolor='rgb(200,200,200)',
            title=dict(
                font=dict(
                    family="Verdana",
                    size=22,
                    color='rgb(19,38,57)',
                )
            ),
            xaxis=dict(
                title=dict(
                    font=dict(
                        family="Verdana",
                        size=16,
                        color='rgb(50,58,83)',
                    ),
                ),
                showgrid=True,
                gridwidth=1,
                gridcolor='rgb(210,210,210)',
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='rgb(220,220,220)',
                ticks="outside",
                tick0=-50,
                dtick=10,
                tickcolor='rgb(19,38,57)',
                visible=True,
            ),
            yaxis=dict(
                title=dict(
                    font=dict(
                        family="Helvetica",
                        size=16,
                        color='rgb(50,58,83)',
                    ),
                ),
                showgrid=True,
                gridwidth=1,
                gridcolor='rgb(210,210,210)',
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='rgb(220,220,220)',
                ticks="outside",
                tick0=0,
                dtick=10,
                tickcolor='rgb(19,38,57)',
                visible=True,
            ),
        )
    )
    return scatter_template
