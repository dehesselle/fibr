CREATE TABLE IF NOT EXISTS files (
    d_name TEXT,
    f_modified INTEGER,
    f_name TEXT,
    f_size INTEGER,
    f_type INTEGER,
    _row_ts INTEGER
);

CREATE INDEX IF NOT EXISTS fully_qualified_name
ON files (
    d_name,
    f_name
);
