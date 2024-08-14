import setuptools

setuptools.setup(
    name="context_extender",
    version="0.0.1",
    author="Oficina EOL UChile",
    author_email="eol-ing@uchile.cl",
    description="A context extension tool for Open edX.",
    long_description="A Django app that adds additional data to the context in specific parts of the Open edX platform.",
    url="https://eol.uchile.cl",
    packages=setuptools.find_packages(),
    install_requires=[
        "eolcourseprogram-xblock @ git+https://github.com/eol-uchile/eol-course-program-xblock@c412c4ffec907a044a23027bf4336cf3450afc64#egg=eolcourseprogram-xblock",
        "eol_sso_login @ git+https://github.com/eol-uchile/eol_sso_login@6f719a689b99bde73f438577d79a614cb53dac2a#egg=eol_sso_login"
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
