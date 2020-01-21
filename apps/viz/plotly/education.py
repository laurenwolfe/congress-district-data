from apps.viz.plotly import templates
from apps.db.DBHandler import DBHandler
from plotly import colors
import plotly.graph_objects as go
import pandas as pd

SQL_PATH = '../sql/'


def external_sql_to_data_frame(query_file, dbh):
    query = open(SQL_PATH + query_file, 'r')
    query_df = pd.read_sql_query(query.read(), dbh.conn)
    dbh.close()

    for i, row in query_df.iterrows():
        cook_pvi = row["cook_pvi"].split("+")
        if cook_pvi[0] == "R":
            pvi = int(cook_pvi[1])
        elif cook_pvi[0] == "D":
            pvi = int(cook_pvi[1]) * -1
        else:
            pvi = 0
        query_df.loc[i, "pvi"] = pvi

    return query_df


def style_chart(query_df):
    scatter_template = go.layout.Template(
        layout=go.Layout(
            plot_bgcolor='rgb(200,200,200)',
            title=dict(
                font=dict(
                    family="Verdana",
                    size=22,
                    color='rgb(19,38,57)',
                )
            )
        )
    )

    fig = go.Figure(
        data=go.Scatter(
            x=query_df['pvi'],
            y=query_df['pct_bachelors'],
            mode='markers',
            text=query_df['district_id'],
            marker_colorscale=colors.sequential.RdBu,
            marker=dict(
                size=10,
                cmax=50,
                cmin=-50,
                color=query_df['pvi'],
                colorscale="RdBu",
                reversescale=True
            ),
        )
    )

    fig.update_layout(
        # template=scatter_template,
        title_text=""
    )

    fig.update_xaxes(
        title_text="Relative partisonship of district (using Cook PVI scale)"
    )

    fig.update_yaxes(
        title_text="% of population with at least bachelors degree"
    )

    fig.show()


def main():
    dbh = DBHandler()
    query_df = external_sql_to_data_frame('education.sql', dbh)
    style_chart(query_df)


if __name__ == "__main__":
    main()
