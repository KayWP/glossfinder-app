CREATE TABLE IF NOT EXISTS glosses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term TEXT,
    indicator TEXT,
    glossed_as TEXT,
    pre_context TEXT,
    post_context TEXT,
    page TEXT
);

CREATE TABLE IF NOT EXISTS clusters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term TEXT,
    count INT
);

-- Create temporary table matching your CSV structure
CREATE TEMP TABLE IF NOT EXISTS temp_glosses (
    term TEXT,
    indicator TEXT,
    glossed_as TEXT,
    pre_context TEXT,
    post_context TEXT,
    page TEXT
);

.mode csv
.import preprocessed_csv.csv temp_glosses

INSERT INTO glosses (term, indicator, glossed_as, pre_context, post_context, page)
SELECT term, indicator, glossed_as, pre_context, post_context, page
FROM temp_glosses;

DROP TABLE temp_glosses;

INSERT INTO clusters (term, count)
SELECT term, COUNT(*) AS count
FROM glosses
GROUP BY term;
