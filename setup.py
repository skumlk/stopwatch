import os
from setuptools import setup, find_packages

setup(
    name = "Stopwatch",
    version = "1.0",
    author = "Sameera Kumarasingha",
    author_email = "sameerakumarasingha@gmail.com",
    description = "Ubuntu Stop Watch",
    license = "BSD",
    url = "https://github.com/skumlk/stopwatch.git",
    packages=['app', 'app.bin', 'app.shared', 'app.img'],
    include_package_data = True,
    package_data = {
        '' : ['*.png'],
    },
    entry_points = {
        'gui_scripts' : ['Stopwatch = app.main:main']
    },
    data_files = [
        ('share/applications/stopwatch', ['Stopwatch.desktop']),
        ('share/icons/hicolor/scalable/apps', ['icon.png']),#main icon
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)