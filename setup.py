"""Setup configuration for structkit-pre-commit hooks."""
from setuptools import setup

setup(
    name='structkit-pre-commit',
    version='1.0.0',
    description='Pre-commit hooks for StructKit YAML structure validation',
    author='Kenneth Belitzky',
    author_email='',
    url='https://github.com/httpdss/structkit-pre-commit',
    license='Apache-2.0',
    py_modules=['structkit_validate_hook', 'structkit_lint_hook'],
    python_requires='>=3.8',
    install_requires=['structkit'],
    entry_points={
        'console_scripts': [
            'structkit-validate-hook=structkit_validate_hook:main',
            'structkit-lint-hook=structkit_lint_hook:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
