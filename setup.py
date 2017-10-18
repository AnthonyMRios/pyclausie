from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pyclausie',
      version='0.1',
      description='Python wrapper around ClausIE (http://www.mpi-inf.mpg.de/departments/databases-and-information-systems/software/clausie/)',
      long_description=readme(),
      url='https://github.com/AnthonyMRios/pyclausie',
      author='Anthony Rios',
      author_email='anthonymrios@gmail.com',
      classifiers=[
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English'
      ],
      license='Apache 2.0',
      packages=['pyclausie'],
      zip_safe=False)
