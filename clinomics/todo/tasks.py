import http.client
import json

from celery import shared_task


@shared_task
def send_email(email, text):
    """
    this is just dummy function that will trigger callback url with email and text
    """
    params = {"email": email, "text": text}
    headers = {
        "Content-type": "application/json"
    }
    conn = http.client.HTTPConnection("127.0.0.1", port=8000)
    conn.request("POST", "/api/v1/email", json.dumps(params), headers)
    response = conn.getresponse()
    status, reason, data = response.status, response.reason, response.read()
    conn.close()

    print(f"status={status} || reason={reason} || data = {data}")

