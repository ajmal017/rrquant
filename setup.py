from setuptools import setup
setup(name='rrquant',
        version='0.1',
        description='A package containing classes and functions made for financial and big data analysis',
        url='https://github.com/RRQuanticaAnalytics/rrquant',
        author='RRQuanticaAnalytics',
        author_email='rohan@rrquanticacapital.com',
        license='MIT',
        install_requires = [
                'pandas',
                'numpy',
                'datetime',
        ],
        packages=['rrquant'],
        zip_safe=False)	
