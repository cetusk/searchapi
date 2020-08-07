# _Usage_

### 1. Import this module.
```python
import searchapi as sapi
```

### 2. Execute.
```python
# create logger instance ( optional )
logs = { "counter": [0], "overwrite": True }
# execute
sapi.search(modulename="numpy", keyname="full", maxdepth=3, strict=False, logger=logs)
```


# _Arguments_

| Name         | Type   | Default | Context |
| :-           | :-:    | :-:     | :- |
| `modulename` | `str`  | ---     | _Fullname_ of a module |
| `keyname`    | `str`  | ---     | Keyword for trying to search |
| `maxdepth`   | `int`  | `3`     | Maximum of searching tree depth |
| `strict`     | `bool` | `False` | Differentiation of upper/lower characters |
| `logger`     | `dict` | `None`  | Logging option |