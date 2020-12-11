from setuptools import find_packages, setup


with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

with open('requirements.txt', 'r', encoding='utf-8') as fp:
    requirements = fp.read().splitlines()

with open('requirements-dev.txt', 'r', encoding='utf-8') as fp:
    requirements_dev = fp.read().splitlines()


setup(
    author='Thomas Steinert',
    author_email='hello@chroni.cc',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    description='API server for providing a centralised slothtamer data backend which can be used from multiple devices.',
    extras_require={
        'dev': requirements_dev
    },
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='slothtamer',
    packages=find_packages(),
    python_requires='==3.8.5',
    url='https://github.com/chronicc/slothtamer-server',
    version='0.0.1',
    zip_safe=False
)
