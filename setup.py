from setuptools import setup, find_packages

exec(open('instructions/version.py').read())

setup(
    name='instructions',
    version=globals()['__version__'],
    packages=find_packages(exclude=('tests', 'tests.*')),
    url='https://github.com/maxtepkeev/instructions',
    license=open('LICENSE').read(),
    author='Max Tepkeev',
    author_email='tepkeev@gmail.com',
    description='Working with iterable data structures made easy',
    long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.rst').read(),
    keywords='instructions,commands,operations,actions,tasks,filters,types,datatypes',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
