import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name='rclickatell',
    version=__import__('rclickatell').__version__,
    author='Caktus Consulting Group',
    author_email='solutions@caktusgroup.com',
    packages=find_packages(),
    include_package_data=True,
    exclude_package_data={
        '': ['*.sql', '*.pyc'],
    },
    url='http://github.com/caktus/rapidsms-clickatell/',
    license='BSD',
    description=' '.join(__import__('rclickatell').__doc__.splitlines()).strip(),
    long_description=read_file('README.rst'),
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    install_requires=(
        'rapidsms>=0.18',
        'django>=1.7',
    ),
)
