from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/reviews', methods=['GET'])
def get_reviews():
    return {"message": "Hello from the backend!"}
