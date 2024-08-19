import setuptools

setuptools.setup(
    name="context_extender",
    version="0.0.3",
    author="Oficina EOL UChile",
    author_email="eol-ing@uchile.cl",
    description="A context extension tool for Open edX.",
    long_description="A Django app that adds additional data to the context in specific parts of the Open edX platform.",
    url="https://eol.uchile.cl",
    packages=setuptools.find_packages(),
    install_requires=[
        "eolcourseprogram-xblock @ https://github.com/eol-uchile/eol-course-program-xblock/archive/refs/tags/0.1.1.zip",
        "eol_sso_login @ https://github.com/eol-uchile/eol_sso_login/archive/refs/tags/0.0.3.zip"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "lms.djangoapp": ["context_extender = context_extender.apps:ContextExtenderConfig"]
    },
)
