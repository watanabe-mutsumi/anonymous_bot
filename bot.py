import os
from time import sleep
from slack import RTMClient
from slack.errors import SlackApiError

@RTMClient.run_on(event='message')
def say_hello(**payload):
    target_channel_name = os.environ["TARGET_CHANNEL_NAME"]
    target_channel_id   = os.environ["TARGET_CHANNEL_ID"]

    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if 'text' in data:
        channel_id = data['channel']
        thread_ts = data['ts']

        #01 投稿者に返信する
        try:
            response1 = web_client.chat_postMessage(
                channel=channel_id,
                text=f"{target_channel_name}に匿名で投稿しました。",
                thread_ts=thread_ts,
                icon_emoji=":penguin:"
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is Falseß
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error on reply: {e.response['error']}")

        #02 3秒待ってから名無しで投稿する
        sleep(3)
        try:
            response2 = web_client.chat_postMessage(
                channel=target_channel_id,
                text=data["text"],
                username="名無しさん",
                icon_emoji=":penguin:"
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error on target post: {e.response['error']}")

rtm_client = RTMClient(token=os.environ["SLACK_API_TOKEN"])
rtm_client.start()