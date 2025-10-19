from setuptools import setup, find_packages

setup(
    name="deudas-app",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "PySide6==6.9.*",
        "pydantic==2.11.*",
        "pydantic-extra-types==2.10.*",
        "email-validator==2.2.*",
        "phonenumbers==9.0.*",
    ],
    entry_points={
        "console_scripts": [
            "deudas-app=src.main:main",
        ],
    },
)
