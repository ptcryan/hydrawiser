""" Hydrawiser setup script """
from setuptools import setup

setup(
    name='Hydrawiser',
    packages=['hydrawiser'],
    version='0.3',
    description='A Python library to communicate with Hunter ' +
                'Wi-Fi irrigation controllers ' +
                '(https://www.hunter.com) that support the ' +
                'Hydrawise application (https://www.hydrawise.com).',
    author='David Ryan',
    author_email='ptcryan@gmail.com',
    url='https://github.com/ptcryan/hydrawiser',
    license='MIT',
    include_package_data=True,
    install_requires=['requests>=2.0'],
    platforms='any',
    test_suite='tests',
    keywords=[
        'sprinkler',
        'water',
        'irrigation',
        'Hunter',
        'Hydrawise'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
