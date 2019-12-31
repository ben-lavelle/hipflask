# hipflask

A small, experimental [Flask](https://palletsprojects.com/p/flask/) webapp to travel with.

> *Built following guidance by [Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world), 2017/18.*

## Storage

We use [flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) and flask-Migration which is a wrapper for the [Alembic](https://github.com/sqlalchemy/alembic) migrations tool.

When making changes to the database structure in [`models.py`](app/models.py), use 

```shell
flask db migrate -m <update message>
flask db upgrade
```

to auto-build the migration script, then apply it to migrate the database.

## Security

For safe password storage and logins we use Pallets' [Werkzeug/security](https://werkzeug.palletsprojects.com/en/0.16.x/utils/#module-werkzeug.security) with [flask-login](https://flask-login.readthedocs.io/en/latest/) for session management.

Werkzeug hashes passwords using [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2) to [key-stretch](https://en.wikipedia.org/wiki/Key_stretching) hashing using SHA256, over 150,000 iterations.
