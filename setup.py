import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eventeditor-GPT",
    version="1.0.4",  # Static version number
    author="leoetlino",
    author_email="leo@leolam.fr",
    description="Event editor for Breath of the Wild and Tears of the Kingdom",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leoetlino/event-editor",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
    include_package_data=True,
    install_requires=[
        'evfl~=1.1',
        'pyqt5-sip~=12.7',
        'pyqtwebengine~=5.14',
        'PyYAML~=5.1',
        'aamp~=1.0',
        'byml~=2.0',
        'oead~=1.1',
    ],
    python_requires='>=3.6',
    entry_points={
        'gui_scripts': [
            'eventeditor = eventeditor.__main__:main'
        ],
    },
)
