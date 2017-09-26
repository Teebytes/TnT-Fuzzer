from setuptools import setup, find_packages

version = open('tntfuzzer/__init__.py', 'r').readline().split()[2].strip("'")

setup(
    name = 'tntfuzzer',
    packages = find_packages(exclude=['*.tests.*']),
    version = version,
    description = 'An OpenAPI (Swagger) fuzzer written in python. Basically TnT for your API.',
    author = 'Tobias Hassenklöver',
    author_email = 'tnt@teebytes.net',
    url = 'https://github.com/Thoiz/TnT-Fuzzer',
    keywords = ['openapi', 'swagger', 'fuzzer', 'fuzzing', 'json-api', 'REST'],
    install_requires = ['bottle==0.12.13', 'gitdb2==2.0.2', 'GitPython==2.1.5', 'gramfuzz==1.2.0', 'netifaces==0.10.6',
                        'pyaml==17.8.0', 'PyJFuzz==1.1.0', 'pyswagger==0.8.36', 'PyYAML==3.12', 'six==1.10.0',
                        'smmap2==2.0.3', 'validate-email==1.3'])