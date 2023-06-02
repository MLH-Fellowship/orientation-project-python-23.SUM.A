from flask import jsonify

def get_experience_by_index(data, index):
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
    return None

def get_education_by_index(data, index):
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
    return None

def get_skill_by_index(data, index):
    index = int(index)
    if 0 <= index < len(data["skill"]):
        skill = data["skill"][index]
        return jsonify({"name": skill.name,
                        "proficiency": skill.proficiency,
                        "logo": skill.logo,
                        })
    return None
