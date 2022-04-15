import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="igt-tools-sylvainloiseau",
    author_email="sylvain.loiseau@univ-paris13.fr",
    author="Sylvain Loiseau",
    version="0.1.0",
    description="Importer for IGT (interlinear glossed texts).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.univ-paris13.fr/sylvain.loiseau/igt-tools",
    project_urls={
        "Bug Tracker": "https://gitlab.univ-paris13.fr/sylvain.loiseau/igt-tools",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"igttools": "src"},
    packages=["igttools"],
    #packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)

