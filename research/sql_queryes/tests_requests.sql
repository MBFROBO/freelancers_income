select * from freelancers

-- Как распределяется доход фрилансеров в зависимости от региона проживания?
SELECT AVG(earnings_usd) as avg_earnings_usd, client_region as region from freelancers group by client_region order by avg_earnings_usd DESC;
-- Какой процент фрилансеров, считающих себя экспертами, выполнил менее 100 проектов?

WITH total_freelancers AS (
    SELECT COUNT(freelancer_id) AS total FROM freelancers WHERE experience_level = 'Expert'
),
filtered_freelancers AS (
    SELECT COUNT(freelancer_id) AS count FROM freelancers WHERE job_completed < 100 and experience_level = 'Expert'
)
SELECT 
    (filtered.count * 100.0) / total.total AS percent
FROM 
    filtered_freelancers filtered, total_freelancers total;

-- Какая профессиональная категория фрилансеров имеет самый высокий процент успешных завершений проектов?
SELECT AVG(Job_Success_Rate) as avg_job_rate, job_category from freelancers group by job_category order by avg_job_rate DESC;

-- Какие платформы демонстрируют наибольшие средние показатели заработков у фрилансеров?
SELECT AVG(earnings_usd) as income_avg, platform from freelancers group by platform order by income_avg DESC;

-- Существует ли корреляция между уровнем опыта фрилансера и средним рейтингом, полученным от клиентов?

with _grouped AS (
SELECT 
    CASE experience_level
        WHEN 'Intermediate' THEN 2
        WHEN 'Expert' THEN 3
        WHEN 'Beginner' THEN 1
    END as experience_level,
    client_rating
FROM freelancers)
SELECT CORR(experience_level, client_rating) as correlate FROM _grouped

-- Как маркетинговые расходы влияют на количество выполненных проектов у фрилансеров?

SELECT CORR(marketing_spend, job_completed) as correlation from freelancers


-- Какие типы проектов связаны с наибольшей продолжительностью выполнения в днях?
select AVG(job_duration_days) as avg_duration, project_type from freelancers group by project_type order by avg_duration desc;

