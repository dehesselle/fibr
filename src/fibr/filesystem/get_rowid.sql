SELECT rowid
FROM files
WHERE
    f_name = :f_name
    AND d_name = :d_name
