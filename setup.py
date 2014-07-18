# -*- coding: utf-8 -*-
try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    import setuptools

setuptools.setup(
    name='atomhopper',
    version='0.1.0',
    description='Python bindings or interacting with AtomHopper',
    author='',
    author_email='',
    url='https://github.com/rackerlabs/python-atomhopper',
    license='ASLv2',
    install_requires=[
        "pecan",
    ],
    test_suite='atomhopper',
    zip_safe=False,
    include_package_data=True,
    packages=setuptools.find_packages(exclude=['ez_setup']),
    entry_points={
        'console_scripts': [
            'ahc = atomhopper.cli:run'
        ],
    },
)
