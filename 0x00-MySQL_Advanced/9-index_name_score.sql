-- Creates index idx_name_first_score on names
-- table for name's first letter and score.

CREATE INDEX idx_name_first_score ON names(name(1), score);
