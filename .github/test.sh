#!/bin/bash

set -e

pip install -e git+https://github.com/eol-uchile/eol-course-program-xblock@0.1.1#egg=eolcourseprogram-xblock
pip install -e git+https://github.com/eol-uchile/eol_sso_login@0.0.3#egg=eol_sso_login
pip install -e /openedx/requirements/app

cd /openedx/requirements/app
cp /openedx/edx-platform/setup.cfg .
mkdir test_root
cd test_root/
ln -s /openedx/staticfiles .

cd /openedx/requirements/app

DJANGO_SETTINGS_MODULE=lms.envs.test EDXAPP_TEST_MONGO_HOST=mongodb pytest context_extender/tests.py
