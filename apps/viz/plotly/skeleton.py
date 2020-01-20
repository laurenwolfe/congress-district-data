from apps.viz.plotly import templates
from apps.db.DBHandler import DBHandler
from plotly import colors
import plotly.graph_objects as go
import pandas as pd

SQL_PATH = 'sql/'


def external_sql_to_data_frame(query_file, dbh):
    query = open(SQL_PATH + query_file, 'r')
    query_df = pd.read_sql_query(query.read(), dbh.conn)
    dbh.close()
    return query_df


def style_chart(query_df):

    """
    EXAMPLE: GROUPED BAR
    bar_1_df = query_df[query_df[''] == '']
    bar_2_df = query_df[query_df[''] == '']


    fig = go.Figure(
        data=[
            go.Bar(
                x=bar_1_df[''],
                y=bar_1_df[''],
                name='',
                marker=dict(
                    color='rgb(158,202,225)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=1.5,
                    )
                ),
            ),
            go.Bar(
                x=bar_2_df[''],
                y=bar_2_df[''],
                name='',
                marker=dict(
                    color='rgb(33,33,33)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=1.5,
                    )
                ),
            ),
        ])

    fig.update_layout(
        template=templates.style_grouped_bar(),
        title_text="",
    )
    """

    """
    EXAMPLE: SCATTERPLOT
    fig = go.Figure(
        data=go.Scatter(
            x=query_df[''],
            y=query_df[''],
            mode='markers',
            text=query_df[''],
            marker_colorscale=colors.sequential.RdBu,
            marker=dict(
                size=16,
                cmax=40,
                cmin=-40,
                color=query_df[''],
                colorscale="RdBu",
            ),
            hoverinfo="text+x+y",
        )
    )

    fig.update_layout(
        template=templates.style_scatterplot,
        title_text="",
    )
    """

    # fig.show()


def main():
    dbh = DBHandler()
    query_df = external_sql_to_data_frame('EXAMPLE.sql', dbh)
    style_chart(query_df)


if __name__ == "__main__":
    main()
