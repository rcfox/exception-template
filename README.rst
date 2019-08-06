=================
ExceptionTemplate
=================

Raise exceptions with consistent messages while avoiding the boiler plate.

Compare this:

>>> from exception_template import ExceptionTemplate
>>> class MyException(ExceptionTemplate):
...    message = 'Hello, {person}. Here is my {adjective} exception class.'
>>> raise MyException(person='Ryan', adjective='fancy')
Traceback (most recent call last):
    ...
MyException: Hello, Ryan. Here is my fancy exception class.


To this:

>>> class MyException(Exception):
...     def __init__(self, person: str, adjective: str) -> None:
...         self.person = person
...         self.adjective = adjective
...         super().__init__('Hello, {person}. Here is my {adjective} exception class.'
...                          .format(person=person, adjective=adjective))
>>> raise MyException('Ryan', 'lame')
Traceback (most recent call last):
    ...
MyException: Hello, Ryan. Here is my lame exception class.


Or this:

>>> class MyException(Exception):
...     pass
>>> raise MyException('Hello, Ryan. Here is my exception class with a message I copy-pasted in 500 places.')
Traceback (most recent call last):
    ...
MyException: Hello, Ryan. Here is my exception class with a message I copy-pasted in 500 places.


Additionally, the ExceptionTemplate parameters are available as members on the exception instance:

>>> try:
...     foo()
... except MyException as ex:
...    print(ex.person)
Ryan


Installing
==========

``pip install exception-template``

No extra dependencies are needed!
