SELECT rowid
FROM files
WHERE d_name = :d_name AND f_name LIKE :f_name
