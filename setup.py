from setuptools import setup, find_packages

setup(
    name='bridge',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-migrate',
        'flask-sqlalchemy',
        'gunicorn',
        'psycopg2-binary',
        'flask-talisman',
        'alembic',
        'click',
        'blinker',
        'itsdangerous',
        'Jinja2',
        'MarkupSafe',
        'SQLAlchemy',
        'typing-extensions',
        'zipp',
    ],
    entry_points={
        'console_scripts': [
            'bridge=Backend.api.bridge:app',
        ],
    },
)
