import json


def compose_image_prompt(query, image_data):

    txt1 = "Azure data about the image {image_data} \n." \
           "\n query about the image: {query}. " \
           "\nstart the sentence with \"it appears to be\". Explain it to me like I'm a five year old kid ".format(query=query, image_data=image_data)
    return txt1