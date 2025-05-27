DROP TABLE IF EXISTS freelancers;
CREATE TABLE frilancers (
    Freelancer_ID numeric,
    Job_Category varchar,
    Platform varchar,
    Experience_Level varchar,
    Client_Region varchar,
    Payment_Method varchar,
    Job_Completed numeric,
    Earnings_USD numeric,
    Hourly_Rate real,
    Job_Success_Rate real,
    Client_Rating real,
    Job_Duration_Days numeric,
    Project_Type varchar,
    Rehire_Rate real,
    Marketing_Spend numeric
);
Select * from freelancers;