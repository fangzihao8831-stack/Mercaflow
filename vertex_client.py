# -*- coding: utf-8 -*-
"""
Centralized Vertex AI client for MercaFlow.
Reads project + location from env, falls back to known-good defaults.
"""
import os
from google import genai

# Defaults — overridable via env
PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT', 'project-a1331a0f-a61c-4d85-adb')
LOCATION = os.environ.get('GOOGLE_CLOUD_LOCATION', 'global')

# Models — Gemini 3 preview models live on the global endpoint only
PLANNING_MODEL = os.environ.get('PLANNING_MODEL', 'gemini-3-flash-preview')
GENERATION_MODEL = os.environ.get('GENERATION_MODEL', 'gemini-3-pro-image-preview')


def get_client():
    """
    Returns a Vertex AI genai.Client.
    Auth comes from Application Default Credentials (gcloud auth application-default login).
    """
    return genai.Client(
        vertexai=True,
        project=PROJECT,
        location=LOCATION,
    )
