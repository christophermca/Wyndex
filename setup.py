import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wyndex",
    version="0.0.1",
    author="Christopher McAdams",
    author_email="mca.christopher@gmail.com",
    description="Keeping the codebase clean",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/christophermca/Wyndex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
