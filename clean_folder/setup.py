from setuptools import setup, find_namespace_packages

setup(
    name="clean_folder",
    version="1.0",
    author="Volodymyr",
    descriptions="Clean folder script",
    entry_points={'console_scripts': ['clean_folder=clean_folder.clean:main']},
    license="MIT",
    packages=find_namespace_packages(),
)
