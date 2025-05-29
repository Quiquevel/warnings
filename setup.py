import setuptools
from version import __version__

setuptools.setup(
    name = "warnings",
    version = __version__,
    author = "Carlos Murcia Ruiz",
    author_email = "carlosfernando.murcia@gruposantander.com",
    description = "A microservice to get warnings of microservices",
    long_description = "Proactively identify and warn about potential issues in OpenShift projects to prevent critical production incidents.",
    long_description_content_type = "text/markdown",
    url = "http://mypythonpackage.com",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
    ],
    python_requires = '>=3.11.5',
)
