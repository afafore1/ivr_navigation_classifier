import hashlib

from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask('IVR NAVIGATION CLASSIFIER')
auth_key = 'Openapikey'


@app.route("/classify", methods=['POST'])
def classify():
    open_api_key = request.headers.get(auth_key)
    if not open_api_key:
        return jsonify({"error": "Authorization token missing"}), 401
    client = OpenAI(api_key=open_api_key)
    data = request.get_json()
    transcript = data['transcript']
    transcript_hash = hashlib.sha256(transcript.encode()).hexdigest()
    print(transcript_hash)
    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": "This GPT is designed to classify transcripts of calls between a caller and "
                                          "a representative. It will identify and categorize the final state of the "
                                          "call based on predefined outcomes, such as STILL_ON_HOLD, GOT_THROUGH_IVR, "
                                          "FAILED_IVR_NAVIGATION, and more. The GPT should analyze the transcript "
                                          "text to determine the correct classification and provide an accurate "
                                          "assessment of the call's status. It can also add new classifications that "
                                          "sound reasonable based on the provided transcript. The responses should be "
                                          "concise and to the point."},
            {"role": "user", "content": transcript}
        ]
    )

    response = completion.choices[0].message

    return jsonify(response.content)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
