#!/bin/bash
export DJANGO_SETTINGS_MODULE=evaluaciones_nombre_estudiantes.settings
python manage.py collectstatic --noinput
