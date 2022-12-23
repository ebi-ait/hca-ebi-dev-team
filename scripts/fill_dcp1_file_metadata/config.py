import os
from typing import get_type_hints


class AppConfigError(Exception):
    pass


class ConfigUrlConflictError(Exception):
    pass


class Config:
    INGEST_TOKEN: str = None
    LOG_LEVEL: str = 'INFO'
    AZUL_BASE: str = 'https://service.azul.data.humancellatlas.org'
    INGEST_BASE: str = 'https://api.ingest.archive.data.humancellatlas.org'

    def __init__(self, env):
        self.load(env)

    def load(self, env):
        for field in self.__annotations__:
            if not field.isupper():
                continue
            # Raise AppConfigError if required field not supplied
            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError('The {} field is required'.format(field))
            # Cast env var value to expected type and raise AppConfigError on failure
            var_type = get_type_hints(Config)[field]
            try:
                value = var_type(env.get(field, default_value))
                self.__setattr__(field, value)
            except ValueError:
                raise AppConfigError(f'Unable to cast value of "{env[field]}" to type "{var_type}" for "{field}" field')

        if self.APIs_are_conflicting():
            raise ConfigUrlConflictError(f'Azul and Ingest should both point to production or staging. Current URLs '
                                         f'provided: \n- Ingest: {self.INGEST_BASE} \n- Azul: {self.AZUL_BASE}')

    def reload(self):
        self.load(os.environ)

    def APIs_are_conflicting(self):
        if ("dev" in self.AZUL_BASE) == (any([env in self.INGEST_BASE for env in ['dev', 'staging']])):
            return False
        return True
