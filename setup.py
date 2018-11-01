from setuptools import setup


def get_deps():
    return open('requirements.txt', 'r').read().splitlines()


setup(
    name='dashboard',
    version='0.0.1',
    author='Team 5499',
    author_email='bhsrobot@gmail.com',
    description=('A python-flask based smart dashboard for FRC.'),
    license='BSD',
    packages=['dashboard'],
    # install_requires=get_deps(),
    package_data={
        'dashboard': ['static/', 'templates/'],
    },
    entry_points={
        'console_scripts': [
            'dashboard=dashboard:start',
        ],
    },
)
