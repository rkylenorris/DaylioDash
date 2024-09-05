create view v_daily_avgs
as
Select
day,
round(avg(mood_value),2) as avg_mood_value
FROM
   ( SELECT
       day
    ,mood_value
    FROM v_entry_details)
group by date
order by date desc