CREATE TABLE public.posts_scraped (
    body text,
    time text,
    hash text PRIMARY KEY,
    location text,
    title text
);
COPY public.posts_scraped(body, time, hash, location, title)
FROM '/docker-entrypoint-initdb.d/output.csv'
DELIMITER ','
CSV HEADER;