select dps.district_id,
       d.state,
       d.district_num,
       dps.report_year,
       ds.cook_pvi,
       (dps.total_below_50_pct * 1.0 / total) * 100  as pct_below_50,
       (dps.total_below_125_pct * 1.0 / total) * 100 as pct_below_125,
       (dps.total_below_150_pct * 1.0 / total) * 100 as pct_below_150,
       (dps.total_below_185_pct * 1.0 / total) * 100 as pct_below_185,
       (dps.total_below_200_pct * 1.0 / total) * 100 as pct_below_200,
       (dps.total_below_300_pct * 1.0 / total) * 100 as pct_below_300,
       (dps.total_below_400_pct * 1.0 / total) * 100 as pct_below_400,
       (dps.total_below_500_pct * 1.0 / total) * 100 as pct_below_500,
       dps.total
from district_poverty_summary dps
inner join
  district d
     on
       dps.district_id = d.id
inner join
  district_summary ds
    on
       dps.district_id = ds.district_id
where dps.report_year = 2018
  and dps.district_id != 792;