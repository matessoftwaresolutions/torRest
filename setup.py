# from distutils.core import setup
from setuptools import setup, find_packages

VERSION = open('VERSION', 'r').read().strip()
PROJECT_NAME = 'tornado-rest-handler'

tests_require = [
    'nose',
    'coverage',
]

install_requires = [
    'tornado==3.0.1',
    'python-rest-handler==0.0.2',
]

setup(name='%s' % PROJECT_NAME,
      url='https://github.com/AMongeMoreno/%s' % PROJECT_NAME,
      author="aMonge",
      author_email='andres.monmor@gmail.com',
      keywords='python tornado rest handler',
      description='A simple Python Tornado handler that manage Rest requests automatically.',
      license='MIT',
      classifiers=[
          'Framework :: Tornado',
          'Operating System :: OS Independent',
          'Topic :: Software Development'
      ],

      version='%s' % VERSION,
      install_requires=install_requires,
      tests_require=tests_require,
      # test_suite='runtests.runtests',
      # extras_require={'test': tests_require},

      packages=find_packages(),
)

