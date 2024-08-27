from lms.djangoapps.grades.models import PersistentCourseGrade
from lms.djangoapps.certificates.models import GeneratedCertificate
from courseware.courses import get_course_with_access
from opaque_keys.edx.keys import CourseKey

from eol_sso_login.models import SSOLoginExtraData
from eolcourseprogram.models import EolCourseProgram

from django.urls import resolve

import logging
logger = logging.getLogger(__name__)

from statistics import mean

from .utils import calculate_grade

def add_student_program_grade(request):
    context = {}   
    # Get the current view name
    current_view_name = resolve(request.path_info).url_name
    if current_view_name in ['render_cert_by_uuid','preview_cert']:
        # Extract the verification UUID from the request (if available)    
        verification_uuid = request.resolver_match.kwargs.get('certificate_uuid')
        if verification_uuid:
            try:
                # Verified Certificate
                certificate = GeneratedCertificate.objects.get(verify_uuid=verification_uuid)
                course_id = certificate.course_id
                user_id = certificate.user_id
                logger.info(f"Extracted course_id and user_id from certificate with UUID {verification_uuid}: course_id - {course_id}, user_id - {user_id}")
            except GeneratedCertificate.DoesNotExist:
                logger.warning(f"No certificate found with UUID {verification_uuid}")
                return context
        else:
            # Extract course_id from resolver_match kwargs as a fallback
            logger.warning(f"No certificate found with UUID {verification_uuid}")
            return context

        # Fetch the student's grade if we have a course_id
        if course_id and user_id:
            program = EolCourseProgram.objects.filter(final_course_id=course_id).first()
            if program:  # Check if program is not None
                program_courses = program.courses.all()
                if program_courses:  # Check if program_courses is not empty
                    grades = {}
                    scaled_grades = {}
                    for course in program_courses:
                        course_grade = PersistentCourseGrade.objects.filter(user_id=user_id, course_id=course.id).first()
                        grades[str(course.id)] = round(course_grade.percent_grade * 100,3)
                        course_key = CourseKey.from_string(str(course.id))
                        course_info = get_course_with_access(request.user, "load", course_key)
                        grade_cutoff = min(course_info.grade_cutoffs.values()) * 100
                        scaled_grades[str(course.id)] = round(calculate_grade(course_grade.percent_grade * 100, approval_percent=grade_cutoff),3)
                    logger.info(grades)
                    if grades:  # Check if grades list is not empty
                        context['student_program_grades'] = grades
                        context['student_program_scaled_grades'] = scaled_grades
                        context['student_program_percent_grade_avg'] = round(mean(list(grades.values())),3)
                        context['student_program_scaled_grade_avg'] = round(mean(list(scaled_grades.values())),3)
                    else:
                        logger.info('No grades available for the program courses.')
                else:
                    logger.info('No courses found in the program.')
            else:
                logger.info('No program found for the given course_id.')
        else:
            logger.info('No course_id and/or user_id found within the certificate.')
    
    return context


def add_student_grade(request):
    context = {}
    # Get the current view name
    current_view_name = resolve(request.path_info).url_name
    if current_view_name in ['render_cert_by_uuid','preview_cert']:
        # Get the current view name
        current_view_name = resolve(request.path_info).url_name
        # Extract the verification UUID from the request (if available)
        verification_uuid = request.resolver_match.kwargs.get('certificate_uuid')
        if verification_uuid:
            try:
                # Verified Certificate
                certificate = GeneratedCertificate.objects.get(verify_uuid=verification_uuid)
                course_id = certificate.course_id
                user_id = certificate.user_id
                logger.info(f"Extracted course_id from certificate with UUID {verification_uuid}: {course_id}")
            except GeneratedCertificate.DoesNotExist:
                logger.warning(f"No certificate found with UUID {verification_uuid}")
                return context
        else:
            # Extract course_id from resolver_match kwargs as a fallback
            logger.warning(f"No certificate found with UUID {verification_uuid}")
            return context

        # Fetch the student's grade if we have a course_id
        if course_id:
            grade = PersistentCourseGrade.objects.filter(user_id=user_id, course_id=course_id).first()
            if grade:
                context['student_grade'] = grade.percent_grade * 100  # Convert to percentage
            else:
                context['student_grade'] = None
            logger.info(f"Context updated with student grade: {context['student_grade']}")
    
    return context

def add_student_document(request):
    context = {}
    # Get the current view name
    current_view_name = resolve(request.path_info).url_name
    if current_view_name in ['render_cert_by_uuid','preview_cert']:
        verification_uuid = request.resolver_match.kwargs.get('certificate_uuid')
        if verification_uuid:
            try:
                # Verified Certificate
                certificate = GeneratedCertificate.objects.get(verify_uuid=verification_uuid)
                user_id = certificate.user_id
                logger.info(f"Extracted user_id from certificate with UUID {verification_uuid}: user_id - {user_id}")
            except GeneratedCertificate.DoesNotExist:
                logger.warning(f"No certificate found with UUID {verification_uuid}")
                return context
        else:
            # Extract course_id from resolver_match kwargs as a fallback
            logger.warning(f"No certificate found with UUID {verification_uuid}")
            return context
        # Get the current view name
        current_view_name = resolve(request.path_info).url_name        
        # Fetch additional data from eol_sso_login_ssologinextradata
        try:
            extra_data = SSOLoginExtraData.objects.get(user_id=user_id)
            logger.info(f"Context {extra_data.document}")
            context['document'] = extra_data.document
            context['type_document'] = extra_data.type_document
            logger.info(f"Context updated with extra data: document={extra_data.document}, type_document={extra_data.type_document}")
        except SSOLoginExtraData.DoesNotExist:
            logger.warning(f"No extra data found for user_id {user_id}")
            return context
    
    return context
