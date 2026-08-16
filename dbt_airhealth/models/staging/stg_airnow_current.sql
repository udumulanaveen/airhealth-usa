-- Staging model for the AirNow live AQI source.
-- Purpose: 1:1 cleanup of the raw table only — rename columns to
-- snake_case, no joins, no filters, no calculations. This is the
-- single place we'd fix things if AirNow ever changes a column name.

with source as (

    -- Pull everything from the raw source table as-is.
    -- source() tells dbt this table comes from outside dbt (declared
    -- in _sources.yml), not built by another model — this is what
    -- lets dbt draw the lineage graph back to raw data.
    select * from {{ source('airnow', 'raw_airnow') }}

),

renamed as (

    -- Rename every column to snake_case for consistency across the
    -- whole project. Raw AirNow field names are mixed case because
    -- that's how the API returns them — we don't change the source,
    -- only how we refer to it from here on.
    select
        DateObserved     as date_observed,
        HourObserved     as hour_observed,
        LocalTimeZone    as local_time_zone,
        ReportingArea    as reporting_area,
        StateCode        as state_code,
        Latitude         as latitude,
        Longitude        as longitude,
        ParameterName    as parameter_name,
        AQI              as aqi,
        category_number  as category_number,
        category_name    as category_name
    from source

)

-- Final output of this model: the cleaned, renamed AirNow records.
select * from renamed
