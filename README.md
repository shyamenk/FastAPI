# Fast API Notes

1.  **Path Parameters**:

    Path parameters are part of the URL itself, and they are used to identify a specific resource. They are typically used in scenarios where you have a specific resource that you want to access or manipulate.

    ```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/items/{item_id}")
    async def read_item(item_id: int):
        return {"item_id": item_id}
    ```

    In this example, `item_id` is a path parameter. When you make a request to `/items/123`, FastAPI will extract `123` from the URL and pass it as the `item_id` argument to the `read_item` function.

2.  **Query Parameters**:

    Query parameters are additional parameters added to the end of a URL and are used to modify the behavior of the request. They are commonly used for filtering, sorting, or providing additional options to an endpoint.

    ```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/items/")
    async def read_item(skip: int = 0, limit: int = 10):
        return {"skip": skip, "limit": limit}
    ```

    In this example, `skip` and `limit` are query parameters. If you make a request to `/items/?skip=5&limit=20`, FastAPI will automatically extract `skip=5` and `limit=20` from the URL and pass them as arguments to the `read_item` function.

**When to Use Which**:

- Use path parameters when you want to identify a specific resource. For example, when retrieving a specific user by their ID.
- Use query parameters when you want to provide optional parameters or filters for an endpoint. For example, when paginating through a list of items and you want to specify the page size and offset.

Remember that both path and query parameters can be used in the same endpoint, and FastAPI will automatically handle extracting the values from the URL and passing them as arguments to your function.

Here's an example of an endpoint that uses both path and query parameters:

python

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int, skip: int = 0, limit: int = 10):
    return {"item_id": item_id, "skip": skip, "limit": limit}
```

In this example, `item_id` is a path parameter, while `skip` and `limit` are query parameters. This endpoint allows you to retrieve information about a specific item (`item_id`), and optionally specify pagination parameters (`skip` and `limit`).
