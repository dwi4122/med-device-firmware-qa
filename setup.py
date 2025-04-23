from setuptools import setup, find_packages

setup(
    name="cpap-firmware-simulator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'influxdb',
        'robotframework',
    ],
)