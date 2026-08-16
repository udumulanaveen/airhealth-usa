-- dim_station: one row per unique AirNow reporting station,
-- sourced from AirNow data (the source with coordinate-level detail).

with source as (

    -- Collapse repeated measurement rows down to one row per unique
    -- station (reporting area + state + coordinates).
    select distinct
        reporting_area,
        state_code,
        latitude,
        longitude
    from {{ ref('stg_airnow_current') }}

)

select
    -- Surrogate key for this dimension, same idea as location_key.
    row_number() over (order by state_code, reporting_area) as station_key,
    reporting_area,
    state_code,
    latitude,
    longitude
from source
