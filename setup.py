from setuptools import setup, find_packages

VERSION = '2.1.1'



# Setting up
setup(
    name="PyCAI2",
    version=VERSION,
    author="Tokai Faclo",
    author_email="otsronca@gmail.com",
    description='Unofficial Python wrapper for character ai, More Easy to use',
    url="https://github.com/FalcoTK/PyCAI2",
    packages=find_packages(),
    install_requires=['curl_cffi', 'websockets', 'easygoogletranslate','pydub'],
    keywords=['python', 'AI', 'chat bot', 'character ai'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
