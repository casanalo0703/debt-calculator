from setuptools import setup, find_packages

setup(
    name='deudas-app',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # Aquí puedes agregar las dependencias necesarias
    ],
    entry_points={
        'console_scripts': [
            'deudas-app=main:main',  # Cambia 'main' por la función que inicie tu aplicación
        ],
    },
)