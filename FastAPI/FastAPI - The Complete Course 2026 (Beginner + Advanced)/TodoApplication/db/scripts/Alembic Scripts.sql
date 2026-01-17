SELECT * FROM `users`;
DESCRIBE `users`;
SELECT * FROM alembic_version;

-- to delete a particular version
DELETE FROM alembic_version WHERE version_num = (SELECT version_num FROM alembic_version);
-- to drop the entire table
DROP TABLE alembic_version;



-- alter table users drop column phone_number;