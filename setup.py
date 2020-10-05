from setuptools import setup

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='bazema_linker',
    author='Baptiste Azéma',
    author_email='baptiste@azema.tech',
    version='1.0',
    packages=['bazema_linker', 'bazema_linker.utils'],
    include_package_data=True,
    python_requires='~=3.6',
    install_requires=REQUIREMENTS,
    description='TODO.',
    license='LICENSE',
    entry_points={
        'console_scripts': ['bazema_linker=bazema_linker.__main__:main']
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
