'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill

app = Flask(__name__)

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


@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Handle experience requests
    '''

    if request.method == 'GET':
        index = request.args.get("index")
        if index is not None:
            index = int(index)
            if 0 <= index < len(data["experience"]) - 1:
                exp = data["experience"][index]
                return jsonify({"title": exp.title,
                                "company": exp.company,
                                "start_date": exp.start_date,
                                "end_date": exp.end_date,
                                "description": exp.description,
                                "logo": exp.logo,
                                })
        return jsonify(data["experience"])

    if request.method == 'POST':
        req = request.get_json()
        new = Experience(req["title"],
            req["company"],
            req["start_date"],
            req["end_date"],
            req["description"],
            req["logo"]
        )

        data["experience"].append(new)
        return jsonify({"id": data["experience"].index(new)})


@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})
