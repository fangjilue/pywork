from setuptools import find_packages, setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='selector',
    version='1.0.0',
    author="闻西",
    author_email="fangjilve@mgzf.com",
    description="定时查询系统余额",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        'flask','pymysql','apscheduler',
    ],
)