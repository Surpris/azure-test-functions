"""
setup.py
"""

from setuptools import setup, find_packages

AUTHOR_NAME = 'Surpris'

setup(
    name='azure-test-functions',
    version='0.1.0',
    description='Functions using the Azure Computer Vision',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url=f'https://github.com/{AUTHOR_NAME}/azure-test-functions',
    author=AUTHOR_NAME,
    author_email='take90-it09-easy27@outlook.jp',
    license='Apache-2.0 License',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
