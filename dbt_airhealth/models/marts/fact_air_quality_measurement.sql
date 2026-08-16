-- fact_air_quality_measurement: one row per actual AQI reading,
-- combining AirNow (station-grain) and EPA (county-grain) data.
-- Each row references dimensions by key instead of repeating text.

with airnow_measurements as (

    -- AirNow's parameter_name already matches dim_pollutant's
    -- pollutant_code directly (e.g. "O3"), no translation needed here.
    select
        date_observed,
        state_code,
        reporting_area,
        parameter_name as pollutant_code,
        aqi,
        category_name
    from {{ ref('stg_airnow_current') }}

),

epa_measurements as (

    -- EPA calls it "Ozone" where AirNow/dim_pollutant use "O3" —
    -- same translation we did when building dim_pollutant.
    select
        date_reported as date_observed,
        state_code,
        county_name,
        case
            when defining_parameter = 'Ozone' then 'O3'
            else defining_parameter
        end as pollutant_code,
        aqi,
        category as category_name
    from {{ ref('stg_epa_daily_aqi') }}

),

airnow_fact as (
    select
        d.date_key,
        cast(null as integer) as location_key,
        s.station_key,
        p.pollutant_key,
        am.aqi,
        am.category_name,
        'airnow' as source_system
    from airnow_measurements am
    left join {{ ref('dim_date') }}      d on am.date_observed  = d.date_day
    left join {{ ref('dim_station') }}   s on am.reporting_area = s.reporting_area
                                           and am.state_code    = s.state_code
    left join {{ ref('dim_pollutant') }} p on am.pollutant_code = p.pollutant_code
),

epa_fact as (
    select
        d.date_key,
        l.location_key,
        cast(null as integer) as station_key,
        p.pollutant_key,
        em.aqi,
        em.category_name,
        'epa' as source_system
    from epa_measurements em
    left join {{ ref('dim_date') }}      d on em.date_observed = d.date_day
    left join {{ ref('dim_location') }}  l on em.state_code    = l.state_code
                                           and em.county_name  = l.county_name
    left join {{ ref('dim_pollutant') }} p on em.pollutant_code = p.pollutant_code
)

select
    row_number() over (order by source_system, date_key) as measurement_key,
    *
from (
    select * from airnow_fact
    union all
    select * from epa_fact
)
