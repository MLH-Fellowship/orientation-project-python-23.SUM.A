'''
Utils file which separates the logic from the app.py router file
'''

import dataclasses
from flask import jsonify
from models import Experience

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

def delete_education_by_index(data, index):
    '''
    Delete and return specific education by index or None if not found
    '''
    index = int(index)
    if 0 <= index < len(data["education"]):
        edu = data["education"].pop(index)
        return jsonify({"course": edu.course,
                        "school": edu.school,
                        "start_date": edu.start_date,
                        "end_date": edu.end_date,
                        "grade": edu.grade,
                        "logo": edu.logo,
                        })
    return jsonify({"Server Error": "Couldn't find needed education"})

def update_education_by_index(data, index, updated):
    '''
    Edit and return specific education by index or None if not found
    '''
    index = int(index)
    if 0 <= index < len(data["education"]):
        data["education"].pop(index)
        data["education"].insert(index, updated)
        return jsonify({"course": updated.course,
                        "school": updated.school,
                        "start_date": updated.start_date,
                        "end_date": updated.end_date,
                        "grade": updated.grade,
                        "logo": updated.logo,
                        })
    return jsonify({"Server Error": "Couldn't find needed education"})

def update_experience_by_index(data, index, new_experience_json):
    '''
    Update an existing experience by index or do nothing if not found
    You can only pass the field you want to change instead of passing a new whole object
    '''
    index = int(index)
    if 0 <= index < len(data["experience"]):
        # Get the fields of the Experience class dynamically instead of hardcoding
        fields_to_update = [field.name for field in dataclasses.fields(Experience)]
        print(fields_to_update)
        # Iterate over each field to update
        for field in fields_to_update:
            # Check if the field exists in new_experience_json
            if field in new_experience_json:
                # Update the corresponding field in the existing experience
                setattr(data["experience"][index], field, new_experience_json[field])
        return jsonify(data["experience"][index])
    return jsonify({"Server Error": "Couldn't find needed experience"})
