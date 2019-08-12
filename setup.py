import setuptools

with open('README.rst') as f:
    long_description = f.read()

setuptools.setup(
    name='exception-template',
    version='1.0.0',
    description='Create exception classes from message templates.',
    long_description=long_description,
    url='https://github.com/rcfox/exception-template',
    author='Ryan Fox',
    author_email='ryan@rcfox.ca',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Typing :: Typed'
    ],
)
