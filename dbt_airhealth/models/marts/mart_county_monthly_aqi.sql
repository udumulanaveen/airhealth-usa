-- mart_county_monthly_aqi: one row per county per month, EPA data
-- rolled up from daily to monthly granularity.

with epa_fact as (
    select * from {{ ref('fact_air_quality_measurement') }}
    where source_system = 'epa'
),

joined as (
    select
        d.year,
        d.month,
        l.state_code,
        l.state_name,
        l.county_code,
        l.county_name,
        f.aqi
    from epa_fact f
    join {{ ref('dim_date') }}     d on f.date_key     = d.date_key
    join {{ ref('dim_location') }} l on f.location_key = l.location_key
)

select
    year,
    month,
    state_code,
    state_name,
    county_code,
    county_name,
    round(avg(aqi), 1) as avg_aqi,
    max(aqi)           as max_aqi,
    min(aqi)           as min_aqi,
    count(*)           as num_days_reporting
from joined
group by year, month, state_code, state_name, county_code, county_name
