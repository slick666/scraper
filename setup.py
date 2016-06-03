from setuptools import setup, find_packages

setup(name='scraper',
      description='Gets video data for pytube/pyvideo-data project',
      author='pytube developers',
      license='Apache License 2.0',
      packages=find_packages(exclude=('tests', 'tests.*')),
      include_package_data=True
      )
