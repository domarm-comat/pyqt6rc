import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyqt6rc",
    version="0.0.1",
    license='MIT',
    author="Martin Domaracký",
    author_email="domarm@comat.sk",
    description="PyQt6 UI templates resource converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/domarm-comat/crawlMpGui",
    packages=setuptools.find_packages(),
    package_data={'crawlMpGui.resources': ['*.*'],
                  'crawlMpGui.templates': ['*.*']},
    scripts=['crawlMpGui/scripts/search_fs_mp_gui'],
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
    extras_requires={
    },
    python_requires='>=3.7',
)
