from logging.config import fileConfig
import importlib
import pkgutil
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from config import settings
from db.database import Base
from sqlalchemy import create_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

engine = create_engine(settings.DB_URI, isolation_level="AUTOCOMMIT")


def import_all_subpackages(module, into_package=__package__):
    if module.__package__ != module.__name__:
        return
    if module.__file__:
        # it is a module (dir has __init__.py)
        pkgpath = os.path.dirname(module.__file__)
    else:
        # it is a namespace (dir don't has __init__.py)
        pkgpath = module.__path__._path[0]
    imported_modules = {}
    for (module_loader, name, is_package) in pkgutil.iter_modules([pkgpath]):
        imported_modules[name] = importlib.import_module(
            module.__name__ + '.' + name, into_package)
    return imported_modules


def import_all_models():
    import models
    return import_all_subpackages(models)


# before get target_metadata need to load ALL models of service to detect changes on them
import_all_models()

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
