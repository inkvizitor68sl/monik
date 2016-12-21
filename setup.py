from setuptools import setup, find_packages

# debian standart library support
requirements = [
    'Flask>=0.8.1',
    'MySQL-python>=1.2.3'
]

setup(
    name='monik',
    version='0.1',
    packages=find_packages(exclude=['tests', 'tests.*']),
    description='Simple monitoring tool by inkvizitor',
    long_description='Uwsgi like application for monitoring.',
    install_requires=requirements,
    include_package_data=True,
    package_data={
        '': ['static/*', 'templates/*']
    },
    entry_points='''
        [console_scripts]
        monik-initdb=monik.initdb:main
    '''
)
