import codecs
import setuptools

extras_require = {
    'tests': [
        'pytest>=2.8',
        'pytest-cov',
    ],
}

setuptools.setup(
    name='comanage_nacha',
    version='0.2.3',
    url='https://github.com/DisruptiveLabs/comanage_nacha',
    author='DisruptiveLabs',
    author_email='team+nacha@comanage.com',
    license='MIT',
    description='NACHA File Generation',
    long_description=codecs.open('README.rst', 'r', encoding='utf-8').read(),
    platforms='any',
    include_package_data=True,
    install_requires=['six'],
    setup_requires=['pytest-runner>=2.0,<3dev'],
    extras_require=extras_require,
    tests_require=extras_require['tests'],
    packages=setuptools.find_packages('.', exclude=('tests', 'tests.*')),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Office/Business :: Financial',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='nose.collector',
)
