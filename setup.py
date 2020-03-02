from setuptools import setup
def readme():
    with open('README.md') as f:
        return f.read()

setup(name='rrquant',
        version='0.1',
        description='A package containing classes and functions made for financial and big data analysis.',
        long_description = readme(),
        classifiers = [

        ],
        url='https://github.com/RRQuanticaAnalytics/rrquant',
        author='RRQuanticaAnalytics',
        author_email='rohan@rrquanticacapital.com',
        license='MIT',
        install_requires = [
                'pandas',
                'numpy',
                'datetime',
                'markdown',
        ],
        packages=['rrquant'],
        include_package_data = True,
        zip_safe=False,
        test_suite = 'nose.collector',
        tests_require = ['nose'])
