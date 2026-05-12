import os
import boto3
from botocore.exceptions import ClientError

_ssm = None
PARAM_PREFIX = "/youtube-x-bot"


def _client():
    global _ssm
    if _ssm is None:
        _ssm = boto3.client("ssm", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    return _ssm


def put_token(key: str, value: str, secure: bool = True) -> None:
    _client().put_parameter(
        Name=f"{PARAM_PREFIX}/{key}",
        Value=value,
        Type="SecureString" if secure else "String",
        Overwrite=True,
    )


def get_token(key: str) -> str | None:
    try:
        result = _client().get_parameter(
            Name=f"{PARAM_PREFIX}/{key}",
            WithDecryption=True,
        )
        return result["Parameter"]["Value"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "ParameterNotFound":
            return None
        raise


def get_last_posted_video_id() -> str | None:
    return get_token("last_video_id")


def set_last_posted_video_id(video_id: str) -> None:
    put_token("last_video_id", video_id, secure=False)
