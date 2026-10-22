# Online Shop
A project to further my Knowledge on Django and Web development



#### Note
- This is intended to be a personal learning project.
I've been learning from the book; "Django 3 By Example <em>Third edition</em>" by Antonio Mele.
It's a very great book that has been my guide to learning Django. :smile:

## Frameworks Used
- Django (Python)

## Runtime and dependencies

Use Python 3.13 (validated with 3.13.17) and Pipenv. From `myshop/`:

```sh
pipenv --python 3.13
pipenv sync
pipenv verify
pipenv run python -m pip check
pipenv run python manage.py check
```

`Pipfile.lock` is regenerated with Pipenv 2026.10.2; the old lock contained
malformed JSON. Django stays on its supported 5.2 LTS line, currently 5.2.18.
Celery 5.6.3, Flower 2.2.0 and their compatible AMQP/Kombu/Billiard/Vine
dependencies replace the unsupported Celery 4 stack. Task names, asynchronous
dispatch and payment processing are unchanged; tasks use `shared_task`.
Run a worker with `pipenv run celery -A myshop worker -l INFO`, and Flower with
`pipenv run celery -A myshop flower`, only against a deliberately configured
broker. Do not expose Flower without authentication and network access controls.

PDF invoices still use WeasyPrint, now 70.0, with CairoSVG 2.9.1 retained.
Install the native Pango/GLib/HarfBuzz/fontconfig and Cairo libraries required
by those packages. On Apple Silicon with existing Homebrew libraries, validation
used `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib`. PDF rendering uses the
existing local invoice template and CSS, not arbitrary untrusted HTML/CSS.
For GHSA-jhhc-3hcp-qhm5 the published affected range is `<=68.1`, with no stated
first patched release; 70.0 is outside that range. This is not a blanket claim
that rendering untrusted documents is safe. Pillow 13.0.0 was selected because
newer advisories also affect 12.3.0.

### Existing schema and settings

The checked-in `shop/0002_translations` migration already moves names, slugs
and descriptions into translation tables. The ORM and translated admin now
match that schema, retaining its table names, columns and unique constraints.
English/Spanish catalogue queries keep existing slug endpoints, English fallback
and alphabetical display without duplicate translated products. Explicit
translation models preserve the existing `unique_together` instead of requiring
Parler's newer generated constraint names. Order field labels match the existing
`0004` migration. No application migrations or stored monetary fields changed;
`AutoField` preserves integer primary keys.

Back up a development database before applying normal Django/dependency
migrations. Do not fake/unapply the translation migration to match the old
out-of-sync models. Development settings require `BRAINTREE_MERCHANT_ID`,
`BRAINTREE_PUBLIC_KEY` and `BRAINTREE_PRIVATE_KEY` and construct a sandbox
gateway. Isolated checks can supply noncredential placeholders and disable local
environment loading with `PYTHON_DOTENV_DISABLED=1`. Configure real secrets,
allowed hosts and debug settings separately before deployment.

Validation covered isolated SQLite migrations with no pending application
migrations, English/Spanish catalogue and admin rendering, cart/order Decimal
accounting, checkout form and payment result pages, unchanged task registration,
and actual native PDF/SVG rendering. No broker, task execution/publication,
payment API calls or mail delivery were used; those integration paths require
separately configured infrastructure.
