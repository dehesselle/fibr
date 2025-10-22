DELETE FROM files
WHERE
    NOT EXISTS (
        SELECT 1 FROM filesstaging AS fs
        WHERE files.d_name = fs.d_name AND files.f_name = fs.f_name
    )
    AND d_name = ?;
