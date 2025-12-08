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
