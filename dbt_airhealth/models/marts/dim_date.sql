-- dim_date: one row per calendar date, generated as a continuous
-- range (not just dates that happen to appear in the data). This
-- lets later analysis spot gaps in reporting, not just list dates
-- that exist.

with date_range as (

    -- Find the earliest and latest date across both staging sources,
    -- so this dimension automatically covers our full data span.
    select
        min(date_col) as min_date,
        max(date_col) as max_date
    from (
        select date_observed as date_col from {{ ref('stg_airnow_current') }}
        union all
        select date_reported as date_col from {{ ref('stg_epa_daily_aqi') }}
    )

),

date_spine as (

    -- Generate one row per day between min_date and max_date.
    select unnest(generate_series(
        (select min_date from date_range),
        (select max_date from date_range),
        interval '1 day'
    )) as date_day

)

select
    -- Surrogate key: a plain integer version of the date (20250801),
    -- used later to join the fact table to this dimension.
    cast(strftime(date_day, '%Y%m%d') as integer) as date_key,
    date_day,
    extract(year from date_day)    as year,
    extract(month from date_day)   as month,
    extract(day from date_day)     as day,
    extract(quarter from date_day) as quarter,
    strftime(date_day, '%A')       as day_name,
    strftime(date_day, '%B')       as month_name,
    case
        when extract(dow from date_day) in (0, 6) then true
        else false
    end as is_weekend
from date_spine
