-- dim_location: one row per unique state/county combination,
-- sourced from EPA data (the only source with county-level detail).

with source as (

    -- The raw staging table has one row per measurement, so the same
    -- county appears many times. DISTINCT collapses that down to one
    -- row per unique state/county combination.
    select distinct
        state_code,
        state_name,
        county_code,
        county_name
    from {{ ref('stg_epa_daily_aqi') }}

)

select
    -- Surrogate key: a simple sequential ID assigned to each unique
    -- county. The fact table will reference this number instead of
    -- repeating the full state/county text on every row.
    row_number() over (order by state_code, county_code) as location_key,
    state_code,
    state_name,
    county_code,
    county_name
from source
