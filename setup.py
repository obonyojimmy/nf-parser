from setuptools import setup

packages = []
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()


setup(
    name="nf_parser",
    version="0.0.1",
    description="parse nextflow syntax to structured pythonic objects",
    url="https://github.com/obonyojimmy/nf-parser",
    author="obonyojimmy <cliffjimmy27@gmail.com>",
    author_email="cliffjimmy27@gmail.com",
    license="MIT",
    include_package_data=True,
    install_requires=requirements,
    packages=packages,
    zip_safe=False
)
