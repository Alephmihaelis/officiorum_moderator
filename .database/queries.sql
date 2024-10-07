INSERT INTO officia (name, description, expire)
VALUES ('ping', 'pongpongpong', '2024-12-10 15:16:17')


INSERT INTO officia (name, description)
VALUES ('poin', 'ppoin poin')

INSERT INTO officia (name, description, expire)
VALUES ('poin', 'ppoin poin', DATE_ADD(NOW(), INTERVAL 30 DAY));

-- Com o campo tipo datetime
INSERT INTO officia (name, description, expire)
VALUES ('poin', 'ppoin poin', variável);

-- Com o campo tipo number
INSERT INTO officia (name, description, expire)
VALUES ('poin', 'ppoin poin', DATE_ADD(NOW(), INTERVAL variável DAY));