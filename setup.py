from distutils.core import setup
setup(name='location_exif_tool',
      version='0.1',
      description='Tool to add batch locations to photos exif data',
      url='http://github.com/khuumi/location_exif_tool',
      author='Daniel Maxson',
      author_email='dsm2157@columbia.edu',
      license='MIT',
      packages=['location_exif_tool'],
      install_requires=[
          'requests',
          'argparse'
      ],
      zip_safe=False,
      scripts=['bin/add_location_exif'],
)