from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='rrquant',
        version='0.1',
        description='A package containing classes and functions made for financial and big data analysis.',
        long_description = readme(),
        url='https://github.com/RRQuanticaAnalytics/rrquant',
        author='RRQuanticaAnalytics',
        author_email='rohan@rrquanticacapital.com',
        license='MIT',
        packages=['rrquant'],
        install_requires = [
                'pandas',
                'numpy',
                'datetime',
                'markdown',
        ],
        #test_suite = 'nose.collector',
        #tests_require = ['nose'],
        #entry_points = {
        #'console_scripts':['rrquant=rrquant.command_line:main'],
        #},
        include_package_data = True,
        zip_safe=False,)
