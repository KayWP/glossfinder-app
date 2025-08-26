CREATE TABLE IF NOT EXISTS "glosses" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "term" TEXT,
    "indicator" TEXT,
    "glossed_as" TEXT,
    "pre_context" TEXT,
    "post_context" TEXT
);

CREATE TABLE IF NOT EXISTS "clusters" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "term" TEXT,
    "count" INT
)

-- Create temporary table matching your CSV structure
CREATE TEMP TABLE temp_glosses (
    "term" TEXT,
    "indicator" TEXT,
    "glossed_as" TEXT,
    "page" TEXT,
    "pre_context" TEXT,
    "post_context" TEXT
);

-- Import CSV into temporary table
.mode csv
.skip 1
.import output.csv temp_glosses

-- Insert data from temp table into main table (excluding the 'page' column)
INSERT INTO glosses (term, indicator, glossed_as, pre_context, post_context)
SELECT term, indicator, glossed_as, pre_context, post_context FROM temp_glosses;

-- Clean up temporary table
DROP TABLE temp_glosses;

-- 