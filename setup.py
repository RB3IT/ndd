import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NewDadsDoor-RB3IT",
    version="0.0.1",
    author="RB3IT",
    author_email="",
    description="Python Implentation of NewDadsDoor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RB3IT/ndd",
    packages=setuptools.find_packages(),

    include_package_data=True,
    package_data = {
        "":[
            "sketches/Bristol Order Verification Form.jpg",
            "sketches/Bristol Order Verification Form.json"]
        },
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
