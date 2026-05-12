import os
import boto3

ses = boto3.client("ses", region_name=os.environ.get("AWS_REGION", "us-east-1"))


def send_approval_email(video: dict, tweet: str, pending_id: str) -> None:
    base_url = os.environ["APPROVAL_BASE_URL"].rstrip("/")
    approve_url = f"{base_url}/bot/approve/{pending_id}/"
    reject_url = f"{base_url}/bot/reject/{pending_id}/"

    body = (
        f"New YouTube video detected!\n\n"
        f"Title: {video['title']}\n"
        f"URL:   {video['url']}\n\n"
        f"Proposed tweet:\n---\n{tweet}\n---\n\n"
        f"Approve: {approve_url}\n"
        f"Reject:  {reject_url}\n"
    )

    ses.send_email(
        Source=os.environ["SES_SENDER_EMAIL"],
        Destination={"ToAddresses": [os.environ["SES_APPROVER_EMAIL"]]},
        Message={
            "Subject": {"Data": f"[Approval] {video['title'][:60]}"},
            "Body": {"Text": {"Data": body}},
        },
    )
    print(f"Approval email sent for: {video['title']}")
