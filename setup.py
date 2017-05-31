from setuptools import setup
import sys

requirements = ['numpy','pandas','pickle','datetime']

# WE MIGHT WANT TO CHANGE SOME OF THIS
if sys.version_info < (2, 7):
    sys.stdout.write("At least Python 3.3 is required.\n")
    sys.exit(1)
'''
elif sys.version_info < (3, 6):
    # typing was added in 3.5, and we rely on critical features that were
    # introduced in 3.5.2+, so for versions older than 3.6 we rely on
    # a backport
    requirements.append('backports.typing')
'''

#import versioneer

setup(
    name='hmis',
    version="0.9",
    #cmdclass="0.9", # Is this right???
    description='Parsing and visualization tools for the HUD-mandated HMIS data format for homelessness data collection.',
    url='https://github.com/mattbellis/hmis',
    author='Matt Bellis and Sara Mahar',
    author_email='mbellis@siena.edu',
    license='MIT',
    packages = ['hmis'],
    #install_requires = requirements,
    #tests_require = ['pytest', 'pytest-cov'],
    classifiers=[ # HAVE TO FIX ALL THIS
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'License :: Public Domain',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.6',
    ],
)
