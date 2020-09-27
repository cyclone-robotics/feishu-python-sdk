import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="feishu-python-sdk",
    version="0.1.1",
    author="Cyclone Chatbot Dev",
    author_email="jingchao.hu@cyclone-robotics.com",
    description="一个用于和飞书开放平台交互的python库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyclone-robotics/feishu",
    install_requires=[
        "pydantic~=1.6.1",
        "Flask~=1.1.2",
        "aiohttp~=3.6.2",
        "requests~=2.24.0",
        "cryptography~=3.1",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
