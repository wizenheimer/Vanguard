import json
import os
import openai
import boto3


def lambda_handler(event, context):
    model_to_use = "text-davinci-003"
    input_prompt = event["body-json"]["input_prompt"]

    openai.api_key = get_api_key()
    response = openai.Completion.create(
        model=model_to_use,
        prompt=input_prompt,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"],
    )
    text_response = response["choices"][0]["text"].strip()
    return {"statusCode": 200, "body": {"response": text_response}}


def get_api_key():
    lambda_client = boto3.client("lambda")
    response = lambda_client.invoke(
        FunctionName=os.environ["FunctionName"], InvocationType="RequestResponse"
    )

    openai_api_key = json.load(response["Payload"])["body"]["api_key"]
    return openai_api_key
