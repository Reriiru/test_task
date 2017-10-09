## More or less stable.

Issues:

* XHR requests still go to habrahabr.ru instead of 127.0.0.1. As such, they remain unparsed. This has to do with API link being in JS, most likely. Finding a way to fix this.

Answer:

* Parse inline JS.

* Parse application/javascript files.

That way we will be sure there is no links to habrahabr.ru left in this proxy.

* Some symbols ('+', for example) are incorrectly displayed.


To run:

```
python manage.py runserver
```