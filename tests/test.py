import unittest
import string
from typing import Any, Mapping, Sequence

from exception_template import ExceptionTemplate

class TestExceptionTemplate(unittest.TestCase):

    def test_required(self) -> None:

        class TestException(ExceptionTemplate):
            message = '{test} {other_test}'

        # Both test and other_test are required arguments.
        with self.assertRaises(TypeError):
            ex = TestException(test='a')

        with self.assertRaises(TypeError):
            ex = TestException(othertest='b')

        ex = TestException(test='a', other_test='b')
        self.assertIsInstance(ex, TestException)

    def test_extra(self) -> None:

        class TestException(ExceptionTemplate):
            message = '{test}'

        # This time, there is no other_test, so this should be rejected.
        with self.assertRaises(TypeError):
            _ = TestException(test='a', other_test='b')

    def test_stringify(self) -> None:

        class TestException(ExceptionTemplate):
            message = 'Hello, {person}. Here is my {adjective} exception class.'

        ex = TestException(person='Ryan', adjective='fancy')
        self.assertEqual(str(ex), 'Hello, Ryan. Here is my fancy exception class.')

    def test_get_attributes(self) -> None:

        class TestException(ExceptionTemplate):
            message = '{test} {other_test}'

        ex = TestException(test='a', other_test='b')
        self.assertEqual(ex.test, 'a')
        self.assertEqual(ex.other_test, 'b')

        with self.assertRaises(AttributeError):
            _ = ex.something_else_entirely

    def test_explicit_init(self) -> None:

        class TestException(ExceptionTemplate):
            message = '{test} {other_test}'

            def __init__(self, pos: int, key: bool = False, **kwargs: str) -> None:
                super().__init__(**kwargs)
                self.pos = pos
                self.key = key
                self.message += str(pos)

        ex = TestException(4, key=True, test='a', other_test='b')
        ex2 = TestException(5, key=True, test='a', other_test='b')

        # Able to deal with explicitly-defined arguments that are not included in the format string.
        self.assertEqual(ex.key, True)
        self.assertEqual(ex.pos, 4)

        # The instances create a shadow of `message` so they don't interfere with each other.
        self.assertEqual(str(ex), 'a b4')
        self.assertEqual(str(ex2), 'a b5')

    def test_child_class_override(self) -> None:

        class ParentException(ExceptionTemplate):
            message = 'Parent {test}'

        class ChildException(ParentException):
            message = 'Child {other_test}'

        ex = ChildException(other_test='a')
        self.assertEqual(str(ex), 'Child a')
        with self.assertRaises(AttributeError):
            _ = ex.test

        self.assertIsInstance(ex, ChildException)
        self.assertIsInstance(ex, ParentException)

    def test_child_class_no_override(self) -> None:

        class ParentException(ExceptionTemplate):
            message = 'Parent {test}'

        class ChildException(ParentException):
            pass

        ex = ChildException(test='a')
        self.assertEqual(str(ex), 'Parent a')

    def test_formatter(self) -> None:

        class AngryFormatter(string.Formatter):
            def vformat(self, format_string: str, args: Sequence[Any],
                        kwargs: Mapping[str, Any]) -> str:
                return super().vformat(format_string, args, kwargs).upper()

        class TestException(ExceptionTemplate):
            message = 'Sometimes I {feeling} to {verb} things.'
            formatter = AngryFormatter()

        ex = TestException(feeling='like', verb='yell')
        self.assertEqual(str(ex), 'SOMETIMES I LIKE TO YELL THINGS.')


if __name__ == '__main__':
    unittest.main()
