DROP TABLE IF EXISTS entry_tags;

CREATE TABLE entry_tags (
    entry_id INTEGER,
    tag TEXT,
    FOREIGN KEY (entry_id) REFERENCES dayEntries(id)
);

-- Insert split tags into the table
INSERT INTO entry_tags (entry_id, tag)
WITH RECURSIVE split(id, tag, rest) AS (
    SELECT id,
           substr(tags, 1, instr(tags || ' ', ' ') - 1) AS tag,
           substr(tags, instr(tags || ' ', ' ') + 1) AS rest
    FROM dayEntries
    WHERE tags != '' and tags not null
    UNION ALL
    SELECT id,
           substr(rest, 1, instr(rest || ' ', ' ') - 1),
           substr(rest, instr(rest || ' ', ' ') + 1)
    FROM split
    WHERE rest != ''
)
SELECT id, tag FROM split;