import setuptools

# https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/
# https://python-packaging.readthedocs.io/en/latest/dependencies.html

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="igtcorpus",
    author_email="sylvain.loiseau@univ-paris13.fr",
    author="Sylvain Loiseau",
    version="0.0.3",
    description="Importer for IGT (interlinear glossed texts).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.univ-paris13.fr/sylvain.loiseau/igtcorpus",
    project_urls={
        "Bug Tracker": "https://gitlab.univ-paris13.fr/sylvain.loiseau/igtcorpus",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"igtcorpus": "src"},
    package_data={"igtcorpus": ["py.typed", 'schema/emeld.dtd']},
    include_package_data=True,
    packages=["igtcorpus"],
    #packages=setuptools.find_packages(where="src"),
    install_requires=[
          'lxml>=4.6.3',
          'pytest>=6.2.5',
          'pympi-ling>=1.70.2',
          'attrs>=21.2.0'
    ],
    # For dependencies not on pyPI:
    #dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0']
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': ['igtc=igtcorpus.cli:igtc']
    }
)

