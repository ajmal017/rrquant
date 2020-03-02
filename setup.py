import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='rrquant',
        version='0.1',
        description='A package containing classes and functions made for financial and big data analysis.',
        long_description = long_description,
        long_description_content_type = 'text/markdown'
        url='https://github.com/RRQuanticaAnalytics/rrquant',
        author='RRQuanticaAnalytics',
        author_email='rohan@rrquanticacapital.com',
        license='MIT',
        packages= setuptools.find_packages(),
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independant",
        ],
        install_requires = [
                'pandas',
                'numpy',
                'datetime',
                'markdown',
        ],
        python_requires = '>=3.6',
        include_package_data = True,
        zip_safe=False,)
