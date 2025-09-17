import json
import requests
from app.schemas.responses import Response
from fastapi import status

ENDPOINTS = [
    '/superusers',
    '/top-countries',
    '/team-insights',
    '/active-users-per-day'
]

class Evaluation:
    def __init__(self):
        pass


    def evaluate_api(self):
        tested_endpoints = []
        with requests.session() as session:
            for endpoint in ENDPOINTS:
                response = session.get(f'http://localhost:8000{endpoint}')
                response = Response(**json.loads(response.text))
                data = {
                    endpoint: {
                        "status": response.status,
                        "time_ms": response.body.execution_time_ms,
                        "valid_response": True if response.status in (200, 201) else False
                    }
                }
                tested_endpoints.append(data)
        response = {
            "status": status.HTTP_200_OK,
            "body": {
                "tested_endpoints": tested_endpoints
            }
        }
        return response
