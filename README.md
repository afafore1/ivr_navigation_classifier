# IVR Navigation Classifier

This Flask application classifies transcripts of calls between a caller and a representative. It uses OpenAI's GPT-4 model to identify and categorize the final state of the call based on predefined outcomes.

## API Usage

### Endpoint: `/state`

- **Method**: `POST`
- **URL**: `https://classifier-c25ygqlvaq-uc.a.run.app/state`
- **Headers**:
  - `Authorization: Bearer YOUR_OPEN_API_KEY`
- **Request Body**:
  ```json
  {
    "transcript": "The caller said..."
  }
- **Response Body**:
  ```json
  {
    "response": "CLASSIFICATION_RESULT",
    "timestamp": "2024-08-01",
    "status": "success"
  }
- **Errors**:
  ```json
  {
    "error": "Authorization token missing or invalid"
  }
- **Errors**:
  ```json
  {
    "error": "Invalid input. Transcript must be provided"
  }

## Considerations
- The transcripts are converted to hash so we can use it as a caching method through the database
  - We do not want to repeat the same calls repeatedly, as each request costs money.
  The negative of using a form of caching is that if our model is updated, we will not leverage that for seen transcripts.
    - The model used is stored so we can re-run the transcripts seen if there is an improvement in the model used.
    - Perhaps we could create the hash based on the model and transcript.

- We could consider updating the request body to allow a user to specify that they do not want to use the cache. This is helpful if the user believes they'll get different responses each time they perform a query
- We could consider allowing the user to provide their prompts to the agent. 
