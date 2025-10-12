SELECT
    rowid,
    f_name,
    f_size,
    f_modified
FROM files AS f1
WHERE
    d_name = :d_name
    -- we don't have cleanup atm and will amass duplicates,
    -- so make sure we get only the newest data
    AND _row_ts = (
        SELECT MAX(f2._row_ts) FROM files AS f2
        WHERE f2.d_name = f1.d_name
    )
ORDER BY
    d_name,
    f_name
