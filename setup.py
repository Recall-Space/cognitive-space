"""
Package configuration.
"""

from setuptools import find_namespace_packages, setup

setup(
    name="cognitive-space",
    version="0.0.1",
    description="The cognitive space package abstracts and stores Recall Space Cognitive Algorithms.",
    url="https://github.com/Recall-Space/cognitive-space",  
    author="Recall Space",
    author_email='info@recall.space',
    license="Open source",
    packages=find_namespace_packages(exclude=["tests"]),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "azure-search-documents<12.0.0",
        "langchain-openai<1.0.0",
        "agent-builder<1.0.0",
        "recall-space-benchmarks<1.0.0",
        "pymongo<5.0.0"
    ],
    test_suite="tests",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.10",
    ],
)