from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cbpi4-pca9685',
      version='0.0.2',
      description='CraftBeerPi4 PCA9685',
      author='Jonathan Tubb',
      author_email='jonathan.tubb@gmail.com',
      url='https://github.com/jtubb/cbpi4-PCA9685',
      license='GPLv3',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-pca9685': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-pca9685'],
	    install_requires=[
            'cbpi>=4.0.0.45',
            'numpy',
            'pca9685_driver'
      ],
      long_description=long_description,
      long_description_content_type='text/markdown'
     )
