from setuptools import setup, find_packages

# read in version from tntfuzzer.py
with open('tntfuzzer/tntfuzzer.py', 'r') as file:
    content = file.readlines()
    for line in content:
        if line.startswith('version'):
            version = line.split('\"')[1]
            break

# read all dependencies and convert them to list
with open('requirements.txt') as file:
    content = file.readlines()
    dependencies = [line.replace('\n', '') for line in content]

setup(
    name='tntfuzzer',
    packages=find_packages(exclude=['tests.*']),
    version=version,
    description='An OpenAPI (Swagger) fuzzer written in python. Basically TnT for your API.',
    author='Tobias Hassenkloever',
    author_email='tnt@teebytes.net',
    url='https://github.com/Teebytes/TnT-Fuzzer',
    keywords=['openapi', 'swagger', 'fuzzer', 'fuzzing', 'json-api', 'REST'],
    entry_points={'console_scripts': ['tntfuzzer=tntfuzzer.tntfuzzer:main']},
    install_requires=dependencies)
