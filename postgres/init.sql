CREATE TABLE public.posts_scraped (
    hash text PRIMARY KEY,
    body text,
    location text,
    title text,
    time text
);
COPY public.posts_scraped(location,body,time,title,hash)
FROM '/docker-entrypoint-initdb.d/output.csv'
DELIMITER ','
CSV HEADER;