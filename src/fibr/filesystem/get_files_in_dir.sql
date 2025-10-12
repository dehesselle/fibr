SELECT
    rowid,
    f_name,
    f_size,
    f_modified
FROM files
WHERE
    d_name = :d_name
ORDER BY
    d_name,
    f_name
