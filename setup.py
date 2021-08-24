from setuptools import find_packages, setup


setup(
    name='electronics-calculator',
    version='0.1',
    packages=['electronics_calculator'],
    install_requires=['electronics_calculator'],
    author='Alan D Moore',
    author_email='alan@alandmoore.com',
    url='https://github.com/alandmoore/electronics_calculator',
    entry_points={
        'console_scripts': [
            'electronics-calculator = electronics_calculator.__main__:main'
        ]
    }
)
