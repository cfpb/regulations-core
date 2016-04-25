from setuptools import setup, find_packages

setup(
    name = "regcore",
    version = "1.2.0", 
    license = "public domain", 
    packages = find_packages(),
    include_package_data=True,
    package_data = {
        'regcore': ['templates/search/indexes/regcore/regulation_text.txt'],
    }
)
