import awsgi
import os
from flask import request,Flask
from service.respond_image_type import get_image_response_service
from utils.llama import query_docx, query_pdf

app = Flask(__name__)
DOCX = "docx"
PDF= "pdf"
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'png','jpeg'}
ALLOWED_DOCUMENT_EXTENSIONS = {PDF, DOCX}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS.union(ALLOWED_DOCUMENT_EXTENSIONS)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def allowed_image_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_IMAGE_EXTENSIONS


def allowed_document_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_DOCUMENT_EXTENSIONS

def is_authenticate(request):
    auth = request.headers.get('Authorization')
    if auth is None:
        return False
    [type, credentials] = auth.split(' ')
    if type != 'Bearer':
        return False
    if credentials != os.environ['API_KEY']:
        return False
    return True

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def foo(path):
    print("foo")
    if not is_authenticate(request):
        print("Unauthenticated")
        return {'error': 'Unauthorized'}, 401

    print("request.files", request.files)
    if 'file' not in request.files:
        print("no file")
        return {"error": "no file part"}
    file = request.files['file']
    if not file or not allowed_file(file.filename):
        return {
                   "error": "file format not supported please send filename with jpg or png for images and pdf or docx for documents"}, 400
    filename, file_type = file.filename.rsplit('.', 1)

    if 'query' not in request.form:
        return {"error": "no query part"}

    if allowed_image_file(file.filename):
        print("image")
        ai_response = get_image_response_service(request, file)
        print("ai_response", ai_response)
        return {
            "message": ai_response
        }
    query = request.form['query']

    if allowed_document_file(file.filename):
        if file_type == DOCX:
            print("query DOCX", query)
            ai_response = query_docx(query, file)
            return {"message": ai_response}
        if file_type == PDF:
            print("query PDF", query)
            ai_response = query_pdf(query, file)
            return {"message": ai_response}



def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/jpeg", "image/png", "application/pdf", "multipart/form-data"})











#
# import json
# from flask import request, Flask
# import awsgi
# app = Flask(__name__)
#
# @app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
# @app.route('/<path:path>', methods=['GET', 'POST'])
# def foo(path):
#     print("foo")
#     print("request.files", request.files)
#     data = {
#         'form': request.data,
#         'args': request.args.copy(),
#         # 'data': request.data,
#         'headers': request.headers.get('Host'),
#         'json': request.json
#     }
#     print("data", data)
#     return (
#         json.dumps(data, indent=4, sort_keys=True),
#         # {"message": "hello world"},
#         200,
#         {'Content-Type': 'application/json'}
#     )
#
#
# def lambda_handler(event, context):
#     return awsgi.response(app, event, context, base64_content_types={"image/png"})
