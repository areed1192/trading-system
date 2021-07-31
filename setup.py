from setuptools import setup
from setuptools import find_namespace_packages

# Open the README file.
with open(file="README.md", mode="r") as fh:
    long_description = fh.read()

setup(

    name='py-trade-system',

    # Define Author Info.
    author='Alex Reed',
    author_email='coding.sigma@gmail.com',

    # Define Version Info.
    version='0.1.0',

    # Define descriptions.
    description='A python application that leverages Microsoft Azure to build a fully functional trading system.',
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Define repo location.
    url='https://github.com/areed1192/trading-system',

    # Define dependencies.
    install_requires=[
        'pyodbc==4.0.31',
        'numpy==1.21.0',
        'requests==2.25.1',
        'pandas==1.2.5',
        'azure-identity==1.6.0',
        'azure-mgmt-core==1.3.0',
        'azure-keyvault-secrets==4.3.0',
        'azure-mgmt-keyvault==9.0.0',
        'msrestazure==0.6.4',
        'azure-mgmt-resource==18.0.0',
        'azure-storage-blob==12.8.1',
        'azure-mgmt-sql==3.0.0',
        'azure-mgmt-storage==18.0.0',
        'azure-mgmt-datafactory==1.1.0'
    ],

    # Specify folder content.
    packages=find_namespace_packages(
        include=[
            'tradesys'
        ]
    ),

    # Define the python version.
    python_requires='>3.9',

    # Define our classifiers.
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8'
    ]

)
