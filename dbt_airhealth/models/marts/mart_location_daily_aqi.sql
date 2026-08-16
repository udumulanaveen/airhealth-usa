-- mart_location_daily_aqi: one row per AirNow station per day,
-- ready to query directly — no joins needed downstream.
-- Reports both the average AQI and the "defining" (worst) pollutant
-- reading, matching how AQI is reported in practice.

with airnow_fact as (
    select * from {{ ref('fact_air_quality_measurement') }}
    where source_system = 'airnow'
),

daily_readings as (

    -- Join the fact table back to its dimensions to get readable
    -- labels, and rank each reading within its station+day group by
    -- AQI (highest = worst = the "defining" reading for that day).
    select
        d.date_day,
        s.reporting_area,
        s.state_code,
        s.latitude,
        s.longitude,
        p.pollutant_name,
        f.aqi,
        f.category_name,
        row_number() over (
            partition by d.date_day, s.reporting_area
            order by f.aqi desc
        ) as aqi_rank
    from airnow_fact f
    join {{ ref('dim_date') }}      d on f.date_key      = d.date_key
    join {{ ref('dim_station') }}   s on f.station_key   = s.station_key
    join {{ ref('dim_pollutant') }} p on f.pollutant_key = p.pollutant_key

),

aggregated as (

    -- Average and max AQI per station per day.
    select
        date_day,
        reporting_area,
        state_code,
        latitude,
        longitude,
        round(avg(aqi), 1) as avg_aqi,
        max(aqi)           as max_aqi,
        count(*)           as num_readings
    from daily_readings
    group by date_day, reporting_area, state_code, latitude, longitude

),

defining_pollutant as (

    -- The single worst reading per station per day (aqi_rank = 1),
    -- which determines the "official" pollutant and category.
    select
        date_day,
        reporting_area,
        pollutant_name as defining_pollutant,
        category_name  as overall_category
    from daily_readings
    where aqi_rank = 1

)

select
    a.date_day,
    a.reporting_area,
    a.state_code,
    a.latitude,
    a.longitude,
    a.avg_aqi,
    a.max_aqi,
    a.num_readings,
    dp.defining_pollutant,
    dp.overall_category
from aggregated a
join defining_pollutant dp
    on a.date_day       = dp.date_day
    and a.reporting_area = dp.reporting_area
