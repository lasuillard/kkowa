import logging
from pprint import pformat

from alembic.autogenerate import compare_metadata, produce_migrations
from alembic.operations import Operations
from alembic.operations.ops import ModifyTableOps
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine

from config import settings

from . import models

logger = logging.getLogger(__name__)


# https://alembic.sqlalchemy.org/en/latest/cookbook.html#run-alembic-operation-objects-directly-as-in-from-autogenerate
# https://stackoverflow.com/questions/67188666/how-to-migrate-sqlalchemy-database-without-generating-migration-script
def migrate_db() -> None:
    """Migrate database."""
    metadata = models.Base.metadata
    engine = create_engine(settings.DATABASE_URL)
    context = MigrationContext.configure(engine.connect())
    migrations = produce_migrations(context, metadata)

    if logger.isEnabledFor(logging.DEBUG):
        diff = compare_metadata(context, metadata)
        logger.debug("migration plan generated: %s", pformat(diff, indent=2))

    operations = Operations(context)
    use_batch = engine.name == "sqlite"
    stack = [migrations.upgrade_ops]
    while stack:
        elem = stack.pop(0)
        if use_batch and isinstance(elem, ModifyTableOps):
            with operations.batch_alter_table(table_name=elem.table_name, schema=elem.schema) as batch_ops:
                for table_elem in elem.ops:
                    batch_ops.invoke(table_elem)

        elif hasattr(elem, "ops"):
            stack.extend(elem.ops)

        else:
            operations.invoke(elem)
