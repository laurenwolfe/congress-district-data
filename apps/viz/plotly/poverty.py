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

    # republican_data = query_df.query('pvi > 0')
    # return republican_data

    return query_df


def style_chart(query_df):
    fig = go.Figure(data=go.Scatter(x=query_df['pvi'],
                                    y=query_df['pct_below_50'],
                                    mode='markers',
                                    text=query_df['state'],
                                    marker_colorscale=colors.sequential.RdBu,
                                    marker=dict(
                                        size=16,
                                        cmax=40,
                                        cmin=-40,
                                        color=query_df['pvi'],
                                        colorscale="RdBu",
                                        reversescale=True
                                    ),
                                    hoverinfo="text+x+y",
                                    )
                    )

    fig.update_layout(
        template=templates.style_scatterplot(),
        title_text="",
    )

    fig.show()


def main():
    dbh = DBHandler()
    query_df = external_sql_to_data_frame('poverty.sql', dbh)
    style_chart(query_df)


if __name__ == "__main__":
    main()
