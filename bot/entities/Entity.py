import abc


class Entity(metaclass=abc.ABCMeta):

    def __db_mapping__(self):
        yield from self.__dict__.items()

    def adapt(self):
        """Converts the entity to a tuple for insertion into the database.
        id is replaced with None to allow the database to generate a new id."""
        return tuple((value if key != "id" else None
                      for key, value in self.__db_mapping__()))

    def convert(self, row):
        for key, value in zip(self.__db_mapping__(), row):
            self.__dict__[key] = value
