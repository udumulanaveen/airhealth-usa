-- mart_state_daily_aqi: one row per state per day, aggregating EPA's
-- county-level daily AQI up to the state level. Also reports the
-- state's worst-reporting county and its defining pollutant, same
-- "worst wins" logic as mart_location_daily_aqi.

with epa_fact as (
    select * from {{ ref('fact_air_quality_measurement') }}
    where source_system = 'epa'
),

joined as (
    select
        d.date_day,
        l.state_code,
        l.state_name,
        l.county_name,
        p.pollutant_name,
        f.aqi,
        f.category_name,
        row_number() over (
            partition by d.date_day, l.state_code
            order by f.aqi desc
        ) as aqi_rank
    from epa_fact f
    join {{ ref('dim_date') }}      d on f.date_key     = d.date_key
    join {{ ref('dim_location') }}  l on f.location_key = l.location_key
    join {{ ref('dim_pollutant') }} p on f.pollutant_key = p.pollutant_key
),

aggregated as (
    select
        date_day,
        state_code,
        state_name,
        round(avg(aqi), 1) as avg_aqi,
        max(aqi)           as max_aqi,
        count(*)           as num_counties_reporting
    from joined
    group by date_day, state_code, state_name
),

worst_county as (
    select
        date_day,
        state_code,
        county_name    as worst_county,
        pollutant_name as defining_pollutant,
        category_name  as overall_category
    from joined
    where aqi_rank = 1
)

select
    a.date_day,
    a.state_code,
    a.state_name,
    a.avg_aqi,
    a.max_aqi,
    a.num_counties_reporting,
    w.worst_county,
    w.defining_pollutant,
    w.overall_category
from aggregated a
join worst_county w
    on a.date_day   = w.date_day
    and a.state_code = w.state_code
