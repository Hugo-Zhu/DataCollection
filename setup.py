from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='datacollection_just_for_hugo',
    version='1.0.0',
    packages=find_packages('src', exclude=['test*','example*']),
    url='https://github.com/Hugo-Zhu/DataCollection',
    license='MIT',
    author='Haohao Zhu',
    author_email='zhuhh17@qq.com',
    description='数据采集包',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pandas', 'LAC', 'bs4',
                     'jieba', 'selenium'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


