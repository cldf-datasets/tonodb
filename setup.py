from setuptools import setup


setup(
    name='cldfbench_tonodb',
    py_modules=['cldfbench_tonodb'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'tonodb=cldfbench_tonodb:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
