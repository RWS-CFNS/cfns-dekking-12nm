--COPY statement to copy all the relevant data from te Modem to the database
\COPY public.conn(mno, "RSRQ", "RSRP", "SINR", type, tijd,  lat, long  ) FROM '/home/cfns/systemtest/modem.csv' DELIMITERS ',' CSV HEADER NULL AS ' ';

--UPDATE statement to change lat, long to geography data type so it can be used on the Map website
UPDATE public.conn set coordinates = ST_GeogFromText('POINT(' || long || ' ' || lat ||')');
