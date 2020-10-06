from setuptools import setup

setup(
    name='pyniviz',
    version='1.1.0',
    packages=['pyniviz'],
    url='https://github.com/robbiemallett/pyniviz',
    license='MIT',
    author='Robbie Mallett',
    install_requires=['pandas',
                      'numpy',
                      'scipy',
                      'matplotlib',
                      'docutils',
                      'Pygments'],
    author_email='robbie.mallett.17@ucl.ac.uk',
    long_description='pyniviz is a Python tool for visualising the output of the SNOWPACK model. For information and a link to the documentation please visit the github page.'
)
