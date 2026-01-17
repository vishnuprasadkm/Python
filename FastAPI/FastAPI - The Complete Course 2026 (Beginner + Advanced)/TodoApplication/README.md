# Pre requisites

## SQL

    **Need to install**
        `databases`, `SQLAlchemy`
    *along with __SQL drivers__ for the DB's*
    sqlite -> _No extra driver is needed, python **includes sqlite3 by default**_
    postgresql -> `psycopg2-binary`
    mysql -> `pymysql`

# SQL QUERY'S

## POST

    ```
    INSERT INTO todos (title, description, priority, complete) VALUES ("test title 1", "test description 1", 4, FALSE)
    ```

## GET

    ```
    SELECT * FROM todos WHERE id = 5
    SELECT title FROM todos WHERE priority >= 3
    SELECT * FROM todos WHERE title = "test"
    ```

## PUT

    ```
    UPDATE todos SET complete=True, priority=1 WHERE id=5
    UPDATE todos SET title="test title 2" WHERE priority=3 AND id=3
    UPDATE todos SET description="test description" WHERE priority=3
    ```

## DELETE

    ```
    DELETE FROM todos WHERE id=5
    ```


# Alembic

## Commands

| Alembic Command                  | Details                                             |
|----------------------------------|-----------------------------------------------------|
| `alembic init <folder name>`     | Initializes a new, generic environment              |
| `alembic revision -m <message>`  | Creates a new revision of the environment           |
| `alembic update <revision #id>`  | Runs upgrade migration to the database              |
| `alembic downgrade -1`           | Runs downgrade migration to the database,           |
|                                  | downgrades the last revision                        |

To remove the alembic history delete the version file and in run a sql query to delete the version or drop the alembic table
    -> DELETE FROM alembic_version WHERE version_num = (SELECT version_num FROM alembic_version);
    -> DROP TABLE alembic_version;
and in terminal run alembic stamp head to rebuild Alembic’s tracking table and set it to “base”.