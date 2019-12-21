# hipflask

Trial small Flask webapp to travel with.

## Storage

We use [flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) and flask-Migration which is a wrapper for the [Alembic](https://github.com/sqlalchemy/alembic) migrations tool.

When making changes to the database structure in [`models.py`](app/models.py), use 

```shell
flask db migrate -m <update message>
flask db upgrade
```

to auto-build the migration script, then apply it to migrate the database.
