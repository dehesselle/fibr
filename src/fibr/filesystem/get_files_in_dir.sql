SELECT
    rowid,
    f_name,
    f_size,
    f_modified,
    CASE f_type
        WHEN 2 THEN 1
        ELSE 2
    END directories_first
FROM files
WHERE
    d_name = :d_name
ORDER BY
    directories_first,
    f_name
