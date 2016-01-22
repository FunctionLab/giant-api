## NetWAS with GIANT API

* If your Python setup already has the `requests` package installed, you can
  simply run NetWAS with:

```
python netwas.py
```

* Otherwise, use `setup.py` first to install any dependencies:

```
python setup.py install           # for virtualenv or global install (may require root)
python setup.py install --user    # for local install (without root)
```

followed by:

```
python netwas.py
```

* Successful execution should yield an output similar to that in
  `expected-output.txt`.
