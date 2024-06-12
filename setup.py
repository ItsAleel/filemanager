# setup.py

from setuptools import setup, find_packages

setup(
    name='file_manager',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pyqt5',
        'watchdog',
        'requests',
        'qroq-cloud-api',
    ],
    entry_points={
        'console_scripts': [
            'file_manager=main:main',
        ],
    },
)
