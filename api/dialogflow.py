import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "tiktok-lmiy-172b3a9cdcfb.json"


def get_response(text_to_be_analyzed):
    DIALOGFLOW_PROJECT_ID = "tiktok-lmiy"
    DIALOGFLOW_LANGUAGE_CODE = "en-US"
    SESSION_ID = "current-user-id"
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(
        text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE
    )
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(
            session=session, query_input=query_input
        )
    except InvalidArgument:
        raise

    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print(
        "Detected intent confidence:", response.query_result.intent_detection_confidence
    )
    print("Fulfillment text:", response.query_result.fulfillment_text)
    return response.query_result


if __name__ == "__main__":
    get_response("hello")
