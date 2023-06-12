'''
Flask Application
'''

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
from models import Experience, Education, Skill
from utils import (
    get_experience_by_index, get_education_by_index,
    get_skill_by_index, update_experience_by_index,
    validate_request, delete_education_by_index,
    update_education_by_index, update_skill_by_index,
    generate_description
)
app = Flask(__name__)
SERVER_ERROR = "Server Error"

 # CORS(app) Enables REST API receive http
 # requests without blocking/restricting
 # the request
CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")

data = {
    "experience": [
        Experience("Software Developer",
                   "A Cool Company",
                   "October 2022",
                   "Present",
                   "Writing Python Code",
                   "example-logo.png")
    ],
    "education": [
        Education("Computer Science",
                  "University of Tech",
                  "September 2019",
                  "July 2022",
                  "80%",
                  "example-logo.png")
    ],
    "skill": [
        Skill("Python",
              "1-2 Years",
              "example-logo.png")
    ]
}

@app.route('/')
@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST', 'PUT'])
def experience():
    '''
    Handles requests for experience. Determines what kind of request method 
    is given and then sends the function off to a handler function which 
    will return the appropriate values back to the front end.
    '''

    if request.method == 'GET':
        return handle_get_experience()

    if request.method == 'POST':
        return handle_post_experience()

    if request.method == 'PUT':
        return handle_put_experience()

    return jsonify({"Server Error": "Couldn't process method"})

def handle_get_experience():
    '''
    Will call and return get_experience_by_index function or return all of the 
    experience objects dependent Upon whether there is an index or not
    '''

    index = request.args.get("index")
    if index is not None:
        return get_experience_by_index(data, index)
    return jsonify(data["experience"])

def handle_post_experience():
    '''
    Will validate the requests of each of the fields to make sure that the user has 
    inputted them correctly. Afterwards, there will be a code checked to return either 
    an error message or append the current data and then return the JSONified object 
    '''

    req = request.get_json()

    generate = request.args.get("chatgpt")
    if generate == "yes":
        generated = generate_exp_description(req["description"])
        return jsonify(generated)

    required_fields = {"title":"string", "company":"string", "start_date":"string" \
                           , "end_date":"string", "description":"string", "logo":"string"}

    code, err_message = validate_request(req, required_fields)

    if code != 0:
        return jsonify({"error": err_message}), code

    new = Experience(req["title"],
                     req["company"],
                     req["start_date"],
                     req["end_date"],
                     req["description"],
                     req["logo"]
                     )

    data["experience"].append(new)

    return jsonify({"id": data["experience"].index(new)})

def handle_put_experience():
    '''
    Will call and return get_experience_by_index function. From there, 
    will check if there is a server error. If a server error exists, 
    it will return that error, if not, will return the 
    function update_experience_by_index
    '''

    index = request.args.get("index")
    if index is not None:
        req = request.get_json()

        generate = request.args.get("chatgpt")
        if "description" in req:
            if generate == "yes":
                generated = generate_exp_description(req["description"])
                return jsonify(generated)

        existing_experience = get_experience_by_index(data, index)
        if SERVER_ERROR in existing_experience.json:
            # will return the server error returned by get_experience_by_index function
            return existing_experience
        return update_experience_by_index(data, index, req)

    return jsonify({"Server Error": "Couldn't process method"})

def generate_exp_description(keyphrases):
    '''
    Generate description from the keyphrases in the job experience
    '''
    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_description(keyphrases),
            max_tokens= 100,
            temperature=0.6,
        )
    result=response.choices[0].text
    return {
        "description": result
    }

@app.route('/resume/education', methods=['GET', 'POST', 'DELETE', 'PUT'])
def education():
    '''
    Handles requests for education. If a GET request is called, will call 
    and return get_education_by_index function or return all of the education 
    objects dependent upon whether there is an index or not. If a POST, will validate 
    the requests of each of the fields to make sure that the user has inputted them correctly
    Afterwards, there will be a code checked to return either an error message or append 
    the current data and then return the JSONified object 
    '''
    if request.method == 'GET':
        return handle_get_education()

    if request.method == 'POST':
        return handle_post_education()

    if request.method == 'DELETE':
        return handle_delete_education()

    if request.method == 'PUT':
        return handle_put_education()

    return jsonify({"Server Error": "Couldn't process method"})

def handle_get_education():
    '''
    Handle education get requests
    '''
    index = request.args.get("index")
    if index is not None:
        return get_education_by_index(data, index)
    return jsonify(data["education"])

def handle_post_education():
    '''
    Handle education post requests
    '''
    req = request.get_json()

    required_fields = {"school":"string", "start_date":"string", "end_date":"string" \
                        , "grade":"string", "logo":"string"}

    code, err_message = validate_request(req, required_fields)

    if code != 0:
        return jsonify({"error": err_message}), code

    new = Education(req["course"],
        req["school"],
        req["start_date"],
        req["end_date"],
        req["grade"],
        req["logo"]
    )
    data["education"].append(new)
    return jsonify({"id": data["education"].index(new)})

def handle_delete_education():
    '''
    Handle education delete requests
    '''
    index = request.args.get("index")
    if index is not None:
        return delete_education_by_index(data, index)
    return jsonify(data["education"])

def handle_put_education():
    '''
    Handle education put requests
    '''
    req = request.get_json()
    updated = Education(req["course"],
        req["school"],
        req["start_date"],
        req["end_date"],
        req["grade"],
        req["logo"]
    )
    index = request.args.get("index")
    if index is not None:
        return update_education_by_index(data, index, updated)
    return jsonify(data["education"])


@app.route('/resume/skill', methods=['GET', 'POST', 'PUT'])
def skill():
    '''
    Handles requests for skill. If a GET request is called, will call and return 
    get_skill_by_index function or return all of the skill objects dependent upon 
    whether there is an index or not. if a POST,will validate the requests of each 
    of the fields to make sure that the user has inputted them correctly Afterwards, 
    there will be a code checked to return either an error message or append the 
    current data and then return the JSONified object 
    '''
    if request.method == 'GET':
        return handle_get_skill()

    if request.method == 'POST':
        return handle_post_skill()

    if request.method == 'PUT':
        return handle_put_skill()

    return jsonify({"Server Error": "Couldn't process method"})


def handle_get_skill():
    '''
    Handle skill get requests
    '''
    index = request.args.get("index")
    if index is not None:
        return get_skill_by_index(data, index)
    return jsonify(data["skill"])

def handle_post_skill():
    '''
    Handle skill post requests
    '''
    req = request.get_json()

    required_fields = {"name":"string", "proficiency":"string", "logo":"string"}

    code, err_message = validate_request(req, required_fields)

    if code != 0:
        return jsonify({"error": err_message}), code

    new = Skill(req["name"], req["proficiency"], req["logo"])
    data["skill"].append(new)

    return jsonify({"id": data["skill"].index(new)})

def handle_put_skill():
    '''
    Handle skill put requests
    '''
    req = request.get_json()
    updated = Skill(req["name"],
        req["proficiency"],
        req["logo"]
    )
    index = request.args.get("index")
    if index is not None:
        return update_skill_by_index(data, index, updated)
    return jsonify(data["skill"])
