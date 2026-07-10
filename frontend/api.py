import requests
import streamlit as st

# Backend URL
BASE_URL = "http://127.0.0.1:8000"


def check_backend():
    """
    Check whether FastAPI backend is running.
    """

    try:

        response = requests.get(
            f"{BASE_URL}/health",
            timeout=5
        )

        return response.status_code == 200

    except Exception:

        return False


def upload_document(file):
    """
    Upload document to backend.
    """

    if not check_backend():

        raise Exception(
            "Backend server is not running."
        )

    files = {
        "file": (
            file.name,
            file.getvalue()
        )
    }

    try:

        response = requests.post(
            f"{BASE_URL}/upload",
            files=files,
            timeout=300
        )

    except requests.exceptions.Timeout:

        raise Exception(
            "Upload timed out."
        )

    except requests.exceptions.ConnectionError:

        raise Exception(
            "Unable to connect to backend."
        )

    except Exception as e:

        raise Exception(str(e))

    if response.status_code != 200:

        try:

            error = response.json()

            raise Exception(
                error.get(
                    "detail",
                    "Upload failed."
                )
            )

        except Exception:

            raise Exception(
                response.text
            )

    return response.json()


def ask_question(question):
    """
    Send question to RAG backend.
    """

    if not check_backend():

        raise Exception(
            "Backend server is not running."
        )

    payload = {
        "question": question
    }

    try:

        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            timeout=180
        )

    except requests.exceptions.Timeout:

        raise Exception(
            "LLM response timed out."
        )

    except requests.exceptions.ConnectionError:

        raise Exception(
            "Unable to connect to backend."
        )

    except Exception as e:

        raise Exception(str(e))

    if response.status_code != 200:

        try:

            error = response.json()

            raise Exception(
                error.get(
                    "detail",
                    "Chat request failed."
                )
            )

        except Exception:

            raise Exception(
                response.text
            )

    return response.json()