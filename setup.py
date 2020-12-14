from setuptools import find_packages, setup


def get_variable(var, path):
    """ Returns the value of a variable from a file. """
    with open(path, 'r', encoding='utf-8') as fp:
        for line in fp.read().splitlines():
            if line.startswith(var):
                return line.split('\'')[1]


def get_content(path, splitlines=False):
    """
    Returns the content from a file.
    If splitlines is true, returns the content as a list.
    """
    with open(path, 'r', encoding='utf-8') as fp:
        if splitlines:
            return fp.read().splitlines()
        else:
            return fp.read()


setup(
    author=get_variable('AUTHOR', 'slothtamer/vars.py'),
    author_email=get_variable('AUTHOR_MAIL', 'slothtamer/vars.py'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    description='API server for providing a centralised slothtamer data backend.',
    install_requires=get_content('requirements.txt', True),
    long_description=get_content('README.md'),
    long_description_content_type='text/markdown',
    name=get_variable('APP_NAME', 'slothtamer/vars.py'),
    packages=find_packages(),
    python_requires='==3.8.5',
    url='https://github.com/chronicc/slothtamer-server',
    version=get_variable('APP_VERSION', 'slothtamer/vars.py'),
    zip_safe=False
)
