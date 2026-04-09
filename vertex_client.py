# -*- coding: utf-8 -*-
"""
Centralized Vertex AI client for MercaFlow.
Round-robins across multiple projects to multiply effective RPM quota.
"""
import os
import itertools
from google import genai

LOCATION = os.environ.get('GOOGLE_CLOUD_LOCATION', 'global')

# Project pool — each project has its own RPM quota
PROJECT_POOL = [
    'project-a1331a0f-a61c-4d85-adb',
    'project-7e9a15c4-687c-4500-917',
    'mercaflow-pool-2',
]

# Models — Gemini 3 preview models live on the global endpoint only
PLANNING_MODEL = os.environ.get('PLANNING_MODEL', 'gemini-3-flash-preview')
GENERATION_MODEL = os.environ.get('GENERATION_MODEL', 'gemini-3-pro-image-preview')

# Round-robin iterator
_project_cycle = itertools.cycle(PROJECT_POOL)


def get_client():
    """
    Returns a Vertex AI genai.Client, cycling through projects
    to spread requests across quota pools.
    """
    project = next(_project_cycle)
    return genai.Client(
        vertexai=True,
        project=project,
        location=LOCATION,
    )
