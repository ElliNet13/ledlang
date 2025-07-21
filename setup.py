from setuptools import setup, find_packages

setup(
    name="ledlang",
    version="0.1.0",
    description="A language for controlling LED animations. Other device must support PLOT and CLEAR calls.",
    author="ElliNet13",
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=['pyserial'],
    entry_points={
        'console_scripts': [
            'ledlang = ledlang.LEDLangTesting:main',
        ],
    },
    license="MIT",
)
