import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyqt6rc",
    version="0.3.1",
    license='MIT',
    author="Martin Domaracký",
    author_email="domarm@comat.sk",
    description="PyQt6 UI templates resource converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/domarm-comat/pyqt6rc",
    packages=setuptools.find_packages(),
    package_data={
        'pyqt6rc.scripts': ['pyqt6rc', 'pyqt6sp'],
        'pyqt6rc.test.myPackage': ["*/*"],
        'pyqt6rc.test.myPackage.resources': ["*/*"],
    },
    scripts=['pyqt6rc/scripts/pyqt6rc', 'pyqt6rc/scripts/pyqt6sp'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
    ],
    install_requires=[
        "pyqt6",
        "pyqt6-tools"
    ],
    python_requires='>=3.7',
)
