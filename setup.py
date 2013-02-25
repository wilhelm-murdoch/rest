from setuptools import setup, find_packages

VERSION='0.1.0'

setup(name='rest',
      version=VERSION,
      description="Building blocks for RESTful APIs.",
      long_description=open("README.rst").read(),
      url='http://github.com/theorm/rest',
      license=open("LICENSE").read(),
      author='Roman Kalyakin',
      author_email='roman@kalyakin.com',
      packages=find_packages(exclude=('tests',)),
      package_data={'':['LICENSE','*.rst']},
      include_package_data=True,
      install_requires=[
        'flask',
      ],
      zip_safe=False,
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
      ],
      tests_require=["nose>=0.10"],
      test_suite = "nose.collector",
)
