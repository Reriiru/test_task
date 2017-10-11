## Current stable.

To run:

```
python manage.py runserver
```

Runs on 127.0.0.1:8000

Fixed:
1. The most severe one. It used to be that my logic would only edit the content of a last tag in a branch. Now it properly edits everything, while not destroying scripts.
2. Just changed parser to mimic browser.
3. Added exception handling.

Added:
The most basic tests.
