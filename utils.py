'''
Utils file which separates the logic from the app.py router file
'''

from flask import jsonify
from spellchecker import SpellChecker

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


def spell_check(data):
    '''
    Spell check on  content added by user
    '''
    spell = SpellChecker()
    corrections = []

    for attr in data:
        for key, value in vars(attr).items():
            if key == 'logo':
                continue

            words = value.split()
            misspelled = spell.unknown(words)

            for word in misspelled:
                # Skip words that contain numbers
                if any(char.isdigit() for char in word):
                    continue
                corrected_word = spell.correction(word)
                corrections.append({"before": word, "after": corrected_word})

    return corrections
