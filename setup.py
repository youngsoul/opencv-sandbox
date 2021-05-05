from setuptools import setup

setup(
    name='opencv-sandbox',
    version='0.1',
    packages=['tests', 'hotspots', 'uielements'],
    url='',
    license='beer',
    author='patrick ryan',
    author_email='pat_ryan_99@yahoo.com',
    description='opencv sandbox of utilities',
    install_requires = [
        'opencv-python',
        'numpy'
    ]
)
