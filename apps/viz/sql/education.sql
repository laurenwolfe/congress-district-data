select dps.district_id,
       d.state,
       d.district_num,
       dps.report_year,
       ds.cook_pvi,
       (dpd.not_hs_grad * 1.0 / dps.total) * 100 as pct_not_hs,
       (dpd.hs_or_ged * 1.0 / dps.total) * 100 as pct_hs,
       (dpd.college_to_assoc * 1.0 / dps.total) * 100 as pct_assoc,
       (dpd.bachelors_plus * 1.0 / dps.total) * 100 as pct_bachelors,
       ((dpd.not_hs_grad * 1.0 / dps.total) + (dpd.bachelors_plus * 1.0 / dps.total)) * 100 as pct_not_hs_or_bach,
       ((dpd.hs_or_ged * 1.0 / dps.total) + (dpd.college_to_assoc * 1.0 / dps.total)) * 100 as pct_hs_or_assoc,

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
inner join
  district_poverty_detail dpd
    on
      d.id = dpd.district_id
where dps.report_year = 2018
  and dps.district_id != 792
and dpd.poverty_row = FALSE;