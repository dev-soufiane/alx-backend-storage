-- Defines function SafeDiv to safely divide two numbers,
-- returning 0 if the second is 0.

DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
BEGIN
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN (a / b);
    END IF;
END $$
DELIMITER ;
