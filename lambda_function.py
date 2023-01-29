import requests
import os
import json

tfl_app_key = os.environ["TFL_KEY"]
tfl_app_name = os.environ["TFL_NAME"]
telegram_key = os.environ["TG_KEY"]
telegram_chatid = os.environ["TG_ID"]


tfl_api_baseurl = "https://api.tfl.gov.uk"
lines = ["district"]


def lambda_handler(event, context):
    """
    Send a telegram message if TFL service status is not "Good"
    """

    params = {"app_id": tfl_app_name, "app_key": tfl_app_key, "detail": True}
    msg = ""
    for line in lines:
        url = f"{tfl_api_baseurl}/Line/{line}/Status"
        response = requests.get(url, params=params)
        data = response.json()

        statuses = []
        description = ""
        for i, item in enumerate(data):
            if i > 0:
                description += "\n"
            status = ", ".join(
                [x["statusSeverityDescription"] for x in item["lineStatuses"]]
            )
            if len(item["routeSections"]) > 0:
                status += f"({str(item['routeSections'])})"

            statuses.append({"Line": item["name"], "Status": status})

        if not all([x["Status"] == "Good Service" for x in statuses]):
            msg = str(statuses)

            telegram_params = {
                "chat_id": telegram_chatid,
                "disable_notification": False,
                "text": msg
            }

            r = requests.post(
                f"https://api.telegram.org/bot{telegram_key}/sendMessage",
                params=telegram_params,
                
            )
    return {"statusCode": 200, "body": json.dumps("Hello!")}

