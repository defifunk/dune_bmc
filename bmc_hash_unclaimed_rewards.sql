DROP TABLE IF EXISTS my_table;
CREATE TEMPORARY TABLE my_table AS
SELECT * FROM (VALUES
    (1, 'one'),
    (2, 'two')
) AS t (num, letter);

INSERT INTO my_table (VALUES
    (3, 'three'),
    (4, 'four')
);

SELECT * FROM my_table;