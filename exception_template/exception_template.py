import string

class ExceptionTemplate(Exception):
    message: str = ''
    formatter: string.Formatter = string.Formatter()

    def __init__(self, **kwargs: str) -> None:
        super().__init__()
        self._kwargs = kwargs
        self._error_check()

    def _error_check(self) -> None:
        required = set(arg for _, arg, _, _ in self.formatter.parse(self.message) if arg)
        given = set(self._kwargs.keys())

        missing = required.difference(given)
        if missing:
            raise TypeError('{name} missing requred arguments: {missing}'
                            .format(name=self.__class__.__name__, missing=missing))

        extra = given.difference(required)
        if extra:
            raise TypeError('{name} given extra arguments: {extra}'
                            .format(name=self.__class__.__name__, extra=extra))

    def __str__(self) -> str:
        return self.formatter.format(self.message, **self._kwargs)

    def __getattr__(self, key: str) -> str:
        if key in self._kwargs:
            return self._kwargs[key]
        raise AttributeError("'{name}' object has no attribute '{key}'"
                             .format(name=self.__class__.__name__, key=key))
