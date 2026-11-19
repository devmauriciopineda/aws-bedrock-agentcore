from __future__ import annotations

import argparse
import json
import uuid

import boto3
from botocore.config import Config


def invoke(runtime_arn: str, region: str, profile: str, text: str) -> dict:
    session_id = f"session-{uuid.uuid4().hex}"
    client = boto3.Session(profile_name=profile, region_name=region).client(
        "bedrock-agentcore",
        config=Config(connect_timeout=5, read_timeout=30, retries={"max_attempts": 0}),
    )
    response = client.invoke_agent_runtime(
        agentRuntimeArn=runtime_arn,
        runtimeSessionId=session_id,
        contentType="application/json",
        accept="application/json",
        payload=json.dumps({"input": text, "session_id": session_id}).encode(),
    )
    body = response["response"].read()
    return json.loads(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-arn", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            invoke(args.runtime_arn, args.region, args.profile, args.input),
            ensure_ascii=False,
        )
    )
