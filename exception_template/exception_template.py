import string

class ExceptionTemplate(Exception):
    """
    Base class for templated exceptions. Child classes need only set a format string as the message:

    >>> class MyException(ExceptionTemplate):
    ...     message = 'My exception occurred! Context: {context}'
    >>> raise MyException(context='example')
    Traceback (most recent call last):
        ...
    MyException: My exception occurred! Context: example

    Exception arguments can also be retrieved by name as object members.
    >>> e = MyException(context='example')
    >>> e.context
    'example'

    A custom string formatter can also be supplied to override the default.
    """
    message: str = ''
    formatter: string.Formatter = string.Formatter()

    def __init__(self, **kwargs: str) -> None:
        """
        Exception arguments are accepted as kwargs, but a check is performed to ensure that
        all format string parameters are passed in, and no extras are given.
        """
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
        """
        Any exception kwargs arguments are accessible by name on the object.
        """
        if key in self._kwargs:
            return self._kwargs[key]
        raise AttributeError("'{name}' object has no attribute '{key}'"
                             .format(name=self.__class__.__name__, key=key))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
