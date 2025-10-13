SELECT
    id,
    f_name,
    f_size,
    f_mtime,
    CASE f_type
        WHEN 2 THEN 1
        ELSE 2
    END directories_first
FROM files
WHERE
    d_name = ?
ORDER BY
    directories_first,
    f_name
