from exception_template import ExceptionTemplate

class TestException(ExceptionTemplate):
    message = 'This is a test. {test}'

raise TestException(test='foo')

    
