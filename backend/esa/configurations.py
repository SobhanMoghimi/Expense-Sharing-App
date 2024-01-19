import os

from esa.app.helpers.exceptions.exceptions import DefinitionException
from esa.app.helpers.utils.esa_utils import CommonsUtils


class DatabaseBaseConfig:
    DJANGO_DB_ENGINE: str = "django.db.backends.postgresql"
    RDB_NAME: str = None
    RDB_USERNAME: str = "postgres"
    RDB_PASSWORD: str = "postgres"
    RDB_HOST: str = None
    RDB_PORT = "5432"


class RedisBaseConfig:
    REDIS_HOST: str = None
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = None
    REDIS_DECODE_RESPONSES: bool = True

class ESAConfig(DatabaseBaseConfig, RedisBaseConfig):
    """ Configuration Files for our project. """
    IS_DEBUG: bool = True
    APP_SECRET_KEY: str = None
    ALLOWED_HOSTS: list = []


class Configuration:
    _config_class = ESAConfig

    @classmethod
    def get_all_annotated_fields(cls, clazz):

        all_base_classes = CommonsUtils.all_base_classes(clazz)
        all_inherited_fields = dict()
        for base in all_base_classes:
            if hasattr(base, "__annotations__"):
                for key, value in base.__annotations__.items():
                    all_inherited_fields[key] = value

        return all_inherited_fields

    @classmethod
    def find_dotenv(cls, filename: str, alternative_env_search_dir: str):

        from dotenv import find_dotenv
        file_path = ""
        try:
            file_path = find_dotenv(filename=filename)
        except:
            print("Warning: First try to find .env file failed!")
        if len(file_path) == 0 and alternative_env_search_dir is not None:
            for dirname in CommonsUtils.walk_all_parent_dirs(alternative_env_search_dir):
                check_path = os.path.join(dirname, filename)
                if os.path.isfile(check_path):
                    return check_path

        return file_path

    @classmethod
    def configure(cls, cls_type: type, is_test=False,
                  alternative_env_search_dir: str = None, silent: bool = False):
        """
        Configure project specific configuration for commons lib
        @param cls_type:  Project specific configuration()
        @param is_test:
        @param alternative_env_search_dir:
        """

        cls._config_class = cls_type

        if alternative_env_search_dir is None and not silent:
            print(
                "Warning: alternative_env_search_dir is set to None. .env files can not be found when venv dir located"
                "\noutside of project main directory. you can use alternative_env_search_dir=__file__ to avoid it."
                "\n use silent = True to suppress this warning")
        filename = '.env'
        if is_test:
            filename = '.env.test'

        from dotenv import load_dotenv, dotenv_values
        dotenv_values = dotenv_values(
            cls.find_dotenv(filename=filename, alternative_env_search_dir=alternative_env_search_dir))

        all_annotated_fields = cls.get_all_annotated_fields(cls._config_class)

        for env_attr in dotenv_values:
            if not hasattr(cls._config_class, env_attr):
                # set .env field to class to replace with env values in next loop
                setattr(cls._config_class, env_attr, None)
        load_dotenv(cls.find_dotenv(filename=filename, alternative_env_search_dir=alternative_env_search_dir))
        for attr_name in dir(cls._config_class):
            if attr_name.startswith("__") or callable(getattr(cls._config_class, attr_name)):
                continue

            from_env = os.getenv(attr_name)
            if not from_env:
                continue

            annotated_type = all_annotated_fields.get(attr_name)

            try:
                final_value = cls.set_value_for_class(cls._config_class, attr_name, from_env, annotated_type)
                setattr(cls._config_class, attr_name, final_value)

            except:
                raise DefinitionException(
                    "Configuration field format Exception: For field {} got {}  expected {}.".format(attr_name, str(
                        annotated_type), from_env))

    @classmethod
    def config(cls):
        return cls._config_class

    @classmethod
    def set_value_for_class(cls, clazz, attr_name, env_value: str, annotated_field_class=None):
        class_value = getattr(clazz, attr_name)
        if annotated_field_class:
            if type(annotated_field_class).__name__ != '_GenericAlias':
                if issubclass(annotated_field_class, str):
                    return env_value
            return eval(env_value)

        if class_value:
            return env_value if isinstance(class_value, str) else eval(env_value)
        return env_value
