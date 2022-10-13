import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multibotkit",
    version="0.1.0",
    author="Appvelox LLC",
    author_email="team@appvelox.ru",
    description="Functional library for developing multiplatform chatbots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Appvelox/multibotkit",
    packages=setuptools.find_packages(exclude=["tests*", "examples*"]),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["httpx>=0.23.0", "pydantic>=1.9", "tenacity>=8.0.1", "aiofiles>=22.1.0"],
    extras_require={
        "mongo": ["motor>=3.0.0"],
        "redis": ["aioredis>=2.0.1"]
    },
    python_requires=">=3.7",
)
