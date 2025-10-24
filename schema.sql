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

CREATE TEMP TABLE IF NOT EXISTS temp_glosses (
    "Term" TEXT,
    "Indicator" TEXT,
    "Glossed As" TEXT,
    "Extended Context Pre" TEXT,
    "Extended Context Post" TEXT,
    "Page" TEXT
);

.mode csv
.import preprocessed_csv.csv temp_glosses

INSERT INTO glosses (term, indicator, glossed_as, page, pre_context, post_context)
SELECT "Term", "Indicator", "Glossed As", "Page", "Extended Context Pre", "Extended Context Post"
FROM temp_glosses;

DROP TABLE temp_glosses;

INSERT INTO clusters (term, count)
SELECT term, COUNT(*) AS count
FROM glosses
GROUP BY term;
