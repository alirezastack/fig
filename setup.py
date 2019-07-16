from setuptools import setup, find_packages

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='fig',
    version='0.0.4',
    description='Frontier API Gateway',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Alireza Hosseini',
    author_email='alireza.hosseini@zoodroom.com',
    url='git.zoodroom.com:basket/fig.git',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
