from .azure_vision import analyze
from .open_ai import respond
from .prompt_composer import compose_image_prompt


def get_image_response_service(request, file):
    query = request.form['query']
    print('query', query)
    image_data = analyze(file)
    print("image_data", image_data)
    prompt = compose_image_prompt(query, image_data)
    print("prompt", prompt)
    ai_response = respond(prompt)
    print("ai_response", ai_response)
    return  ai_response
