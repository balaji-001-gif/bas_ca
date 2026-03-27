from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="bas_ca",
    version="1.0.0",
    description="CA & CS Practice Management for Indian firms",
    author="Antigravity",
    author_email="dev@antigravity.in",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
