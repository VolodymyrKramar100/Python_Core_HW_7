from setuptools import setup, find_packages
from os.path import join, dirname

setup(name='clean_folder',
      version='1.0',
      packages=find_packages(),
      long_description=open(join(dirname(__file__), 'README.md')).read(),
      url='',
      author='Volodymyr Kramar',
      entry_points={'console_scripts':
                          ['clean-folder = clean_folder.clean:main']
                    }
)
