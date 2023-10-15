from dynaconf import Dynaconf, Validator

__all__ = ("settings",)

# TODO(lasuillard): Migrate to Pydantic; https://docs.pydantic.dev/latest/concepts/pydantic_settings/
settings = Dynaconf(
    envvar_prefix="KKOWA",
    validators=[
        Validator("DEBUG", cast=bool, default=False),
        Validator("DATABASE_URL", cast=str, required=True, default="sqlite:///./db.sqlite3"),
    ],
)
