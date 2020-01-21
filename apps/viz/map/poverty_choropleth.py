from collections import namedtuple

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as plc
from apps.db.DBHandler import DBHandler
import numpy as np


MapParams = namedtuple(
    'MapParams',
    ['mapped_column', 'val_min', 'val_max', 'norm', 'colors',
     'colorbar_label', 'title', 'annotation', 'output_file']
)


def get_map_df(shp_data):
    map_df = gpd.read_file(shp_data)[['STATEFP', 'CD116FP', 'geometry']]
    map_df.columns = ['state_fips', 'district_num', 'geometry']

    map_df['state_fips'] = map_df['state_fips'].astype(int)
    map_df = map_df[map_df.state_fips <= 56]
    map_df = map_df[map_df.state_fips != 2]
    map_df = map_df[map_df.state_fips != 15]
    # remove geodata for removed districts as of 2010 census (112th congress)
    map_df = map_df[map_df.district_num != 'ZZ']
    map_df['district_num'] = map_df['district_num'].astype(int)
    map_df = map_df.to_crs(epsg=2163)

    return map_df


def get_data_df(sql_path):
    dbh = DBHandler()
    query = open(sql_path, 'r')
    data_df = pd.read_sql_query(query.read(), dbh.conn)
    data_df = data_df[data_df.state_fips <= 56]
    dbh.close()

    for i, row in data_df.iterrows():
        cook_pvi = row["cook_pvi"].split("+")
        if cook_pvi[0] == "R":
            pvi = int(cook_pvi[1])
        elif cook_pvi[0] == "D":
            pvi = int(cook_pvi[1]) * -1
        else:
            pvi = 0
        data_df.loc[i, "pvi"] = pvi

    return data_df


def build_choropleth(map_df, params):
    fig, ax = plt.subplots(1, figsize=(11, 7))

    map_df.plot(
        column=params.mapped_column,
        cmap=params.colors,
        norm=plc.Normalize(params.val_min, params.val_max),
        linewidth=0.3,
        ax=ax,
        edgecolor='0.8',
    )

    ax.axis('off')

    ax.set_title(
        params.title,
        fontdict={'fontsize': '14'}
    )

    ax.annotate(
        params.annotation,
        xy=(0.4, 0.1),
        xycoords='figure fraction',
        horizontalalignment='center',
        verticalalignment="top",
        fontsize=10,
        color='#555555'
    )

    sm = plt.cm.ScalarMappable(
        cmap=params.colors,
        norm=plc.Normalize(params.val_min, params.val_max)
    )
    sm._A = []

    plt.colorbar(
        sm,
        fraction=0.02,
        pad=0.05,
        label=params.colorbar_label
    )

    plt.show()
    fig.savefig(params.output_file, dpi=300)


def main():

    pct_50 = MapParams(
        mapped_column='pct_below_50',
        val_min=1,
        val_max=16,
        colors='YlOrRd',
        colorbar_label='% of Households',
        title='Households with gross income below 50% of poverty line',
        annotation='By congressional district, 2018 US Census Survey Estimates',
        output_file='50pct.png'
    )

    pct_300 = MapParams(
        mapped_column='pct_below_300',
        val_min=55,
        val_max=76,
        colors='YlOrRd',
        colorbar_label='% of Households',
        title='Households with gross income below 300% of poverty line',
        annotation='By congressional district, 2018 US Census Survey Estimates',
        output_file='300pct.png'
    )

    pct_500 = MapParams(
        mapped_column='pct_below_500',
        val_min=34,
        val_max=93,
        colors='YlOrRd',
        colorbar_label='% of Households',
        title='Households with gross income below 500% of poverty line',
        annotation='By congressional district, 2018 US Census Survey Estimates',
        output_file='500pct.png'
    )

    pct_above_500 = MapParams(
        mapped_column='pct_above_500',
        val_min=7,
        val_max=66,
        colors='Greens',
        colorbar_label='% of Households',
        title='Households with gross income above 500% of poverty line',
        annotation='By congressional district, 2018 US Census Survey Estimates',
        output_file='500_above_pct.png'
    )

    cook_pvi = MapParams(
        mapped_column='pvi',
        val_min=-45,
        val_max=45,
        colors='RdBu_r',
        colorbar_label='Cook PVI values',
        title='Relative Partisanship by Congressional District',
        annotation='via Propublica (based on most recent presidential election results)',
        output_file='pvi.png'
    )

    map_df = get_map_df('tl_2018_us_cd116/tl_2018_us_cd116.shp')
    data_df = get_data_df('../sql/map.sql')
    df = data_df.loc[data_df["state"] == 'TX']
    df = df[['state', 'district_num', 'pvi']]
    map_df = map_df.merge(data_df, on=['state_fips', 'district_num'])

    # build_choropleth(map_df, pct_50)
    # build_choropleth(map_df, pct_300)
    # build_choropleth(map_df, pct_above_500)
    build_choropleth(map_df, cook_pvi)


if __name__ == "__main__":
    main()
