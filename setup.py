from setuptools import setup, find_packages

setup(
    name='pycache_handler',
    version='0.1.6',
    packages=find_packages(),
    install_requires=[
        'watchdog'
    ],
    author='Ivan APEDO',
    author_email='apedoivan@gmail.com',
    description='Python package to automatically delete __pycache__ directories.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/iv4n-ga6l/pycache_handler',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)