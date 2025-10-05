from setuptools import setup, find_packages

setup(
    name="ast_roller",
    version="0.1.0",
    py_modules=["grammar", "evaluators", "results"],
    install_requires=["lark==1.1.9"],
)
