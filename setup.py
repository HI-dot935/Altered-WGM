from setuptools import setup, find_packages

setup(
    name="altered-wgm",
    version="1.0.0",
    description="Ultimate OSINT workbench – RAWS + Epieos + Holehe + Xposed + 150+ username sites",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.3.3",
        "flask-cors>=4.0.0",
        "phonenumbers>=8.13.26",
        "dnspython>=2.4.2",
        "requests>=2.31.0",
        "holehe>=2.0.0",
        "aiohttp>=3.9.1",
    ],
    entry_points={"console_scripts": ["altered-wgm=backend.app.cli:main"]},
    python_requires=">=3.9",
)
