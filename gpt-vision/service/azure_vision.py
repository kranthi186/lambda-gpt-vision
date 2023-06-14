import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import os

subscription_key = os.environ["AZURE_SUBSCRIPTION_KEY"]
endpoint =  os.environ["AZURE_COGNITIVE_SERVICES"]

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '{subscription_key}'.format(subscription_key=subscription_key),
}


def analyze(file):
    print("analyze function")
    params = urllib.parse.urlencode({
        # Request parameters
        'features': 'caption,tags,read',
        # 'model-name': '{string}',
        'language': 'en',
        # 'smartcrops-aspect-ratios': '{string}',
        # 'gender-neutral-caption': 'False',
    })
    try:
        image_data = file.read()
        print("image_data line 34", image_data)
        conn = http.client.HTTPSConnection(endpoint)
        conn.request("POST", "/computervision/imageanalysis:analyze?api-version=2023-02-01-preview&%s" % params,
                     image_data,
                     headers)
        response = conn.getresponse()
        data = response.read()
        print("data line 34", data )
        jsonResponse = json.loads(data)
        print("jsonResponse line 34", jsonResponse)
        result = {
            "captionResult": jsonResponse.get("captionResult"),
            "readResult": {
                "stringIndexType": jsonResponse.get("readResult").get("stringIndexType"),
                "content": jsonResponse.get("readResult").get("content")
            },

            "tagsResult": [o.get("name") for o in jsonResponse.get("tagsResult").get("values")]
        }

        conn.close()
        return result


    except Exception as e:
        print(e)
        # print("[Errno {0}] {1}".format(e.errno, e.strerror))
