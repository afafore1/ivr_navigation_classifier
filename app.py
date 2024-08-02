import hashlib
from datetime import datetime

from flask import Flask, request, jsonify
from openai import OpenAI
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()
auth_key = 'Openapikey'


@app.route("/classify", methods=['POST'])
def classify():
    open_api_key = request.headers.get(auth_key)
    if not open_api_key:
        return jsonify({"error": "Authorization token missing"}), 401

    client = OpenAI(api_key=open_api_key)
    data = request.get_json()
    if not data or 'transcript' not in data:
        return jsonify({"error": "Invalid input. Transcript must be provided"}), 400

    transcript = data['transcript']
    transcript_hash = hashlib.sha256(transcript.encode()).hexdigest()
    cached_data = get_cached_data(transcript_hash)
    if cached_data is not None:
        return jsonify(cached_data['response'])

    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": "This GPT is designed to classify transcripts of calls between a caller and "
                                          "a representative. It will identify and categorize the final state of the "
                                          "call based on predefined outcomes. The predefined outcomes are: "
                                          "STILL_ON_HOLD, GOT_THROUGH_IVR, FAILED_IVR_NAVIGATION, CALL_DISCONNECTED, "
                                          "CALL_COMPLETED, CALL_ABORTED_BY_CALLER,"
                                          "CALL_ABORTED_BY_AGENT, CALL_BACK_REQUESTED, "
                                          "and LANGUAGE_SUPPORT_NEEDED. The GPT should analyze the "
                                          "transcript text to determine the correct classification and provide an "
                                          "accurate assessment of the call's status based on these predefined "
                                          "outcomes. The responses should be concise and to the point."},
            {"role": "user", "content": transcript}
        ]
    )

    response = completion.choices[0].message
    content = response.content
    update_transcript_information(transcript_hash, content)

    return jsonify(response.content)


def get_cached_data(transcript_hash):
    doc_ref = db.collection('transcripts').document(transcript_hash)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()

    return None


def update_transcript_information(transcript_hash, response):
    doc_ref = db.collection('transcripts').document(transcript_hash)
    doc_ref.set({
        'transcript_hash': transcript_hash,
        'response': response,
        'timestamp': datetime.utcnow()
    })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
