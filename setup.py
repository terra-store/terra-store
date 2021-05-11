import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="terraform_registry_api", # Replace with your own username
    version="0.0.1",
    author="Jamie Duncombe",
    author_email = "jamie@jduncombe.com",
    description = "Terraform registry API for Terra-store",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/terra-store/terra-store",
    project_urls={
        "Bug Tracker": "https://github.com/terra-store/terra-store/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0 License",
        "Operating System :: Linux",
    ],
    include_package_data=True,
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
)