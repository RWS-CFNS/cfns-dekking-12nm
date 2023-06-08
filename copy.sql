--COPY statement to copy all the data from the Weather station to the PostgreSQL database
\COPY public.weather(winddir, windspeed, druk, humid, temp, dauw, time) FROM 'maximet.csv' DELIMITERS ',' CSV