# context_extender/apps.py

from django.apps import AppConfig
from openedx.core.djangoapps.plugins.constants import PluginSettings, PluginURLs, ProjectType, SettingsType
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ContextExtenderConfig(AppConfig):
    name = 'context_extender'
    verbose_name = "Context Extender"


    plugin_app = {
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common'
                },
            },
        }
    }

    def ready(self):
        pass
