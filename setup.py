from setuptools import setup, find_packages
import sys

# Only need "pygame" on linux
if sys.platform == 'linux':
    setup(
        name='scikit-sound',
        version="0.1.9",
        packages=find_packages(),
    
        include_package_data=True,
        package_data = {'tests': ['*.wav', '*.mp3']},
    
        # Project uses reStructuredText, so ensure that the docutils get
        # installed or upgraded on the target machine
        install_requires=['docutils>=0.3', 'appdirs', 'pygame'],
    
        # metadata for upload to PyPI
        author       = "Thomas Haslwanter",
        author_email = "thomas.haslwanter@fh-linz.at",
        description  = 'Python utilites for working with sound signals',
        long_description=open('README.rst').read(),
        license      = 'http://opensource.org/licenses/BSD-2-Clause',
        download_url = 'https://github.com/thomas-haslwanter/scikit-sound',
        keywords     = 'sound auditory signals',
        url          = 'http://work.thaslwanter.at/sksound/html',
        classifiers  = ['Development Status :: 4 - Beta',
                     'Programming Language :: Python :: 3',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Science/Research',
                     'License :: OSI Approved :: BSD License',
                     'Topic :: Scientific/Engineering'],
        test_suite   = 'nose.collector',
        tests_require=['nose'],
    )
    
else:
    setup(
        name='scikit-sound',
        version="0.1.9",
        packages=find_packages(),
    
        include_package_data=True,
        package_data = {'tests': ['*.wav', '*.mp3']},
    
        # Project uses reStructuredText, so ensure that the docutils get
        # installed or upgraded on the target machine
        install_requires=['docutils>=0.3', 'appdirs'],
    
        # metadata for upload to PyPI
        author       = "Thomas Haslwanter",
        author_email = "thomas.haslwanter@fh-linz.at",
        description  = 'Python utilites for working with sound signals',
        long_description=open('README.rst').read(),
        license      = 'http://opensource.org/licenses/BSD-2-Clause',
        download_url = 'https://github.com/thomas-haslwanter/scikit-sound',
        keywords     = 'sound auditory signals',
        url          = 'http://work.thaslwanter.at/sksound/html',
        classifiers  = ['Development Status :: 4 - Beta',
                     'Programming Language :: Python :: 3',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Science/Research',
                     'License :: OSI Approved :: BSD License',
                     'Topic :: Scientific/Engineering'],
        test_suite   = 'nose.collector',
        tests_require=['nose'],
    )
