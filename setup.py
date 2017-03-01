from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as readmeFile:
    long_description = readmeFile.read()

setup(
    name="mutex_agent",
    description="Agent framework for Mutex",
    long_description=long_description,
    packages=["mutex_agent"],
    include_package_data=True,
    zip_safe=False,
    url="https://github.com/ohsu-comp-bio/gaia_mutex_integration",
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        "Topic :: Utilities"
    ],
    keywords='tool',
    install_requires=[
        "requests==2.13.0",
        "protobuf==3.2.0"

    ],
    entry_points={
        'console_scripts': [
            'mutex-agent=mutex_agent.mutex_agent:main',
            'create-AGM=mutex_agent.create_AGM:main'
        ]
    },
    # Use setuptools_scm to set the version number automatically from Git
    setup_requires=['setuptools_scm'],
    use_scm_version={
        "write_to": "mutex_agent/_version.py"
    },
)
