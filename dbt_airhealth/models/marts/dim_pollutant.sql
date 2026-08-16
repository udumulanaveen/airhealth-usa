-- dim_pollutant: one row per unique pollutant, standardized across
-- both sources. AirNow uses "O3" and EPA uses "Ozone" for the same
-- pollutant, so we map both to one canonical code/name before
-- deduplicating.

with airnow_pollutants as (
    select distinct parameter_name as raw_name
    from {{ ref('stg_airnow_current') }}
),

epa_pollutants as (
    select distinct defining_parameter as raw_name
    from {{ ref('stg_epa_daily_aqi') }}
),

combined as (
    -- Stack both sources' raw pollutant names together.
    select raw_name from airnow_pollutants
    union
    select raw_name from epa_pollutants
),

standardized as (
    -- Map raw source-specific spellings to one canonical code/name.
    -- select distinct here collapses O3 and Ozone into a single row.
    select distinct
        case
            when raw_name in ('O3', 'Ozone') then 'O3'
            else raw_name
        end as pollutant_code,
        case
            when raw_name in ('O3', 'Ozone')  then 'Ozone'
            when raw_name = 'PM10'            then 'Particulate Matter 10'
            when raw_name = 'PM2.5'           then 'Particulate Matter 2.5'
            when raw_name = 'CO'              then 'Carbon Monoxide'
            when raw_name = 'NO2'             then 'Nitrogen Dioxide'
            else raw_name
        end as pollutant_name
    from combined
)

select
    -- Surrogate key assigned only after dedup, so O3/Ozone get one key.
    row_number() over (order by pollutant_code) as pollutant_key,
    pollutant_code,
    pollutant_name
from standardized
