from setuptools import setup, find_packages

setup(
    name="academicjobscraper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4>=4.9.3",
        "requests>=2.25.1",
    ],
    entry_points={
        'console_scripts': [
            'academicjobscraper=academicjobscraper.cli:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A package to scrape and filter academic job listings",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="academic jobs, job scraping, web scraping",
    url="https://github.com/yourusername/academicjobscraper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
