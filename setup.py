import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='XoxoDay',
    version="0.0.31",
    author="Yaşar Özyurt",
    author_email="blueromans@gmail.com",
    description='XoxoDay Api Client For Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blueromans/XoxoDay.git',
    project_urls={
        "Bug Tracker": "https://github.com/blueromans/XoxoDay/issues",
    },
    install_requires=['requests', 'python-dotenv'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['XoxoDay', 'XoxoDay.service', 'XoxoDay.helper'],
    package_data={"": ["*.json"]},
    include_package_data=True,
    python_requires=">=3.6",
)
