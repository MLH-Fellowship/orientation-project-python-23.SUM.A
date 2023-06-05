'''
Utils file which separates the logic from the app.py router file
'''

from flask import jsonify

def get_experience_by_index(data, index):
    '''
    Return specific experience by index or None if not found
    '''
    index = int(index)
    if 0 <= index < len(data["experience"]):
        exp = data["experience"][index]
        return jsonify({"title": exp.title,
                        "company": exp.company,
                        "start_date": exp.start_date,
                        "end_date": exp.end_date,
                        "description": exp.description,
                        "logo": exp.logo,
                        })
    return jsonify({"Server Error": "Couldn't find needed experience"})

def get_education_by_index(data, index):
    '''
    Return specific education by index or None if not found
    '''
    index = int(index)
    if 0 <= index < len(data["education"]):
        edu = data["education"][index]
        return jsonify({"course": edu.course,
                        "school": edu.school,
                        "start_date": edu.start_date,
                        "end_date": edu.end_date,
                        "grade": edu.grade,
                        "logo": edu.logo,
                        })
    return jsonify({"Server Error": "Couldn't find needed education"})

def get_skill_by_index(data, index):
    '''
    Return specific skill by index or None if not found
    '''
    index = int(index)
    if 0 <= index < len(data["skill"]):
        target_skill = data["skill"][index]
        return jsonify({"name": target_skill.name,
                        "proficiency": target_skill.proficiency,
                        "logo": target_skill.logo,
                        })
    return jsonify({"Server Error": "Couldn't find needed skill"})

def delete_skill_by_index(data, index):
    '''
    Delete specific skill by index or None if not found
    '''
    index = int(index)
    if 0 <= index < len(data["skill"]):
        del data["skill"][index]
        return jsonify({"Success": "Skill deleted"})
    return jsonify({"Server Error": "Couldn't find needed skill"})


def validate_request(req, required_fields):
    '''
    Returns an error code and message if the request is invalid
    '''
    missing_fields = [field for field in list(required_fields.keys()) if field not in req]

    if not isinstance(req, dict):
        return 400, "Request data is not valid JSON"
    if missing_fields:
        return 400, f"Missing fields: {', '.join(missing_fields)}"

    # Validate fields types
    for field in list(required_fields.keys()):
        if required_fields[field] == "string":
            if not isinstance(req[field], str):
                return 400, "Some fields have incorrect type"
        if required_fields[field] == "int":
            if not isinstance(req[field], int):
                return 400, "Some fields have incorrect type"

    return 0, ""
