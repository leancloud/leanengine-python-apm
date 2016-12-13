from setuptools import setup, find_packages

setup(
    name='leanengine-apm',
    version='0.0.1',
    description='LeanEnginr APM SDK',

    url='https://leancloud.cn/',

    author='asaka',
    author_email='lan@leancloud.rocks',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='LeanCloud LeanEngine APM',

    packages=find_packages(exclude=['docs', 'tests*']),

    test_suite='nose.collector',

    install_requires=['werkzeug', 'six', 'requests'],

    extras_require={
        'dev': ['sphinx'],
        'test': ['nose', 'wsgi_intercept'],
    }
)
