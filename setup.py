import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="telegraph-next",
    version="1.1.5",
    author="Abbasxan",
    author_email="neongroupmmc@gmail.com",
    description="Modernized Asynchronous Telegraph API wrapper (revived fork)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abbasxan/telegraph-next",
    project_urls={
        "Bug Tracker": "https://github.com/Abbasxan/telegraph-next/issues",
        "Source Code": "https://github.com/Abbasxan/telegraph-next",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.7.4.post0",
        "beautifulsoup4>=4.9.3",
        "bs4>=0.0.1",
        "pydantic>=1.8.2,<2.0.0",
        "urllib3>=1.26.6"
    ],
    include_package_data=True,
    zip_safe=False,
)
