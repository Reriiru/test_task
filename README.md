## More or less stable.

Issues:

* XHR requests still go to habrahabr.ru instead of 127.0.0.1. As such, they remain unparsed.
* Some symbols ('+', for example) are incorrectly displayed.


To run:

```
cd pipeline_task
python manage.py runserver
```
