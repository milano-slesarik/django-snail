from setuptools import setup

setup(name='django-snail',
      version='0.1',
      description='Django middleware that mimics slow responses',
      url='https://github.com/milano-slesarik/django-snail',
      author='Milan Slesarik',
      author_email='milslesarik@gmail.com',
      license='MIT',
      packages=['django_snail'],
      zip_safe=False)