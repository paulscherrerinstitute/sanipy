from setuptools import setup, find_packages

setup(
    name="sanipy",
    version="0.0.1",
    url="https://github.com/augustin_s/sanipy",
    description="A command-line tool for epics connection testing",
    author="Paul Scherrer Institute",
    packages=find_packages(),
    py_modules=["sani", "commands"]
)


