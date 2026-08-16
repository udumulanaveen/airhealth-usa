-- Staging model for the EPA AirData historical AQI source.
-- Same rule as the AirNow staging model: rename columns only,
-- no joins, no filters, no calculations.

with source as (

    -- Raw EPA data, declared as a source in _sources.yml.
    select * from {{ source('epa_airdata', 'raw_epa_aqi') }}

),

renamed as (

    -- EPA's raw column names have spaces in them (e.g. "State Name"),
    -- which is why they're wrapped in double quotes below — DuckDB
    -- requires that for any column name that isn't a single word.
    select
        "State Name"                 as state_name,
        "county Name"                as county_name,
        "State Code"                 as state_code,
        "County Code"                as county_code,
        "Date"                       as date_reported,
        "AQI"                        as aqi,
        "Category"                   as category,
        "Defining Parameter"         as defining_parameter,
        "Defining Site"              as defining_site,
        "Number of Sites Reporting"  as num_sites_reporting
    from source

)

-- Final output: cleaned EPA daily AQI records.
select * from renamed
