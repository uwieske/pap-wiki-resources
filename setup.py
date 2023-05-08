from setuptools import setup

setup(
    name='papwikires',
    version='0.1.0',
    packages=['papwikires'],
    url='',
    license='MIT',
    author='Urso Wieske',
    author_email='uwieske@gmail.com',
    description='Useful resources handling with Wiki data for Papiamento language',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    ### Dependencies
    install_requires=[
        'pandas',
        'wikiextractor',
    ],
    dependency_links=[
    ],
    ### Contents
    # packages=find_packages(exclude=['tests*']),


)
