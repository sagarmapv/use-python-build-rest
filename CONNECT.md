# CONNECT — how `python-quiz-app` topics power this server

Every line of `main.py` traces back to something you already practised.
Open both files side by side and you'll see the same concepts, just with an HTTP wrapper.

---

## Topic 3 — More Control Flow Tools → endpoint handlers

In the quiz app, functions accept arguments, run logic, and return a value.
That's exactly what a FastAPI endpoint is:

```python
# quiz-app style
def greet(name: str) -> str:
    return f"Hello, {name}"

# same idea, HTTP wrapper
@app.get("/items/{item_id}")
def get_item(item_id: str):
    return store[item_id]
```

`if/else` control flow you practised maps directly to the 404 guard:

```python
if item_id not in store:
    raise HTTPException(status_code=404, detail="Item not found")
```

---

## Topic 4 — Data Structures → the in-memory store

The whole "database" is one dict you learned in Topic 4:

```python
store: dict[str, dict] = {}
```

Every CRUD operation is a dict operation you already know:

| HTTP verb | dict operation |
|-----------|---------------|
| POST      | `store[id] = {...}` |
| GET       | `store[id]` |
| PUT       | `store[id] = {new data}` (overwrite) |
| PATCH     | `store[id] = {**old, **patch}` (dict merge) |
| DELETE    | `del store[id]` |

The PATCH merge (`{**existing, **patch}`) is dict unpacking — also Topic 4.

---

## Topic 6 — Input and Output → JSON request / response

Topic 6 covered `input()` / `print()` and file I/O with `open()`.
In a REST API, I/O is HTTP: the request body comes *in* as JSON, the response goes *out* as JSON.

FastAPI handles the serialisation for you (same idea as `json.loads` / `json.dumps` from Topic 6),
but the mental model is identical — read structured data in, write structured data out.

Pydantic models (`ItemCreate`, `ItemPatch`) are the schema that validates the incoming "input",
just like you'd validate a user's `input()` value before using it.

---

## Topic 7 — Errors and Exceptions → HTTPException

Quiz app: `try / except ValueError` when the user types a bad number.
REST API: `raise HTTPException(status_code=404)` when a resource doesn't exist.

Same pattern — detect bad state, raise a typed exception, let the framework handle the response.

---

## New thing this project adds: HTTP verbs

The quiz app ran in a terminal with one user at a time.
A REST API runs as a server that *many* clients call over the network.
The five verbs (`POST GET PUT PATCH DELETE`) are a shared contract — any language, any client,
same URL, same behaviour.

That's the only genuinely new concept here. Everything else is Python you already know.
