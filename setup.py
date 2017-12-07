from setuptools import setup


setup(
    name='Converter',
    version='0.0.1',
    description='Converter for datatypes',
    author='vavatech',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    py_modules=('converter',),
    # install_requires=[],
    entry_points={
        'console_scripts': [
            'converter=converter:main',
        ],
    },
)
