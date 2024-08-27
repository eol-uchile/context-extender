# from django.conf import settings

def plugin_settings(settings):
    # Modify or add to the settings as needed
    settings.TEMPLATES[0]['OPTIONS']['context_processors'].append('context_extender.certificates.context_processors.add_student_grade')
    settings.TEMPLATES[0]['OPTIONS']['context_processors'].append('context_extender.certificates.context_processors.add_student_program_grade')
    settings.TEMPLATES[0]['OPTIONS']['context_processors'].append('context_extender.certificates.context_processors.add_student_document')
