INSERT INTO files (d_name, f_mtime, f_name, f_size, f_type)
SELECT
    fs.d_name,
    fs.f_mtime,
    fs.f_name,
    fs.f_size,
    fs.f_type
FROM filesstaging AS fs
LEFT JOIN files AS f
    ON
        fs.d_name = f.d_name
        AND fs.f_name = f.f_name
ON CONFLICT (d_name, f_name)
DO UPDATE SET
    f_size = excluded.f_size,
    f_mtime = excluded.f_mtime,
    f_type = excluded.f_type;
