'''
Tests in Pytest
'''
from app import app


def test_client():
    '''
    Makes a request and checks the message received is the same
    '''
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"


def test_exp_index():
    '''
    Check if the index of new experience is correct in the list
    '''

    exp1 = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    exp2 = {
        "title": "Accountant",
        "company": "My Company",
        "start_date": "October 2019",
        "end_date": "Present",
        "description": "Filing Taxes",
        "logo": "example-logo.png"
    }

    exp3 = {
        "title": "Lawyer",
        "company": "A Cool Firm",
        "start_date": "October 2020",
        "end_date": "Present",
        "description": "Case Studies",
        "logo": "example-logo.png"
    }

    ind1 = app.test_client().post('/resume/experience',
                                  json=exp1).json['id']
    ind2 = app.test_client().post('/resume/experience',
                                  json=exp2).json['id']
    ind3 = app.test_client().post('/resume/experience',
                                  json=exp3).json['id']

    # check if the correct index is returned
    assert ind1 == 1
    assert ind2 == 2
    assert ind3 == 3

    # check if GET request with index gives the same JSON
    response = app.test_client().get('/resume/experience')
    assert response.json[ind1] == exp1
    assert response.json[ind2] == exp2
    assert response.json[ind3] == exp3

    # check if POST request body has all the required fields and correct types
    incomplete_experience = {
        "title": "Lawyer",
        "company": "A Cool Firm",
        "start_date": "October 2020",
        "end_date": "Present",
        "description": "Case Studies"
    }

    response = app.test_client().post('/resume/experience', json=incomplete_experience)
    assert response.status_code == 400
    assert "Missing fields" in response.json['error']

    invalid_experience = {
        "title": "Lawyer",
        "company": "A Cool Firm",
        "start_date": 1685732137, #Epoch for example
        "end_date": "August 2024",
        "description": "Case Studies",
        "logo": "example-logo.png"
    }

    response = app.test_client().post('/resume/experience', json=invalid_experience)
    assert response.status_code == 400
    assert "Some fields have incorrect type" in response.json['error']


def test_experience():
    '''
    Add a new experience and then get all experiences. 
    
    Check that it returns the new experience in that list
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']
    response = app.test_client().get('/resume/experience')
    assert response.json[item_id] == example_experience


def test_education():
    '''
    Add a new education and then get all educations. 
    
    Check that it returns the new education in that list
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/education',
                                     json=example_education).json['id']

    response = app.test_client().get('/resume/education')
    assert response.json[item_id] == example_education

    incomplete_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "logo": "example-logo.png"
    }

    response = app.test_client().post('/resume/education', json=incomplete_education)
    assert response.status_code == 400
    assert "Missing fields" in response.json['error']

    invalid_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": 1685732137, #Epoch for example
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }

    response = app.test_client().post('/resume/education', json=invalid_education)
    assert response.status_code == 400
    assert "Some fields have incorrect type" in response.json['error']


def test_skill():
    '''
    Add a new skill and then get all skills. 
    
    Check that it returns the new skill in that list
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    response = app.test_client().get('/resume/skill')
    assert response.json[item_id] == example_skill

    correct_response = {"Success": "Skill deleted"}
    response = app.test_client().delete('/resume/skill', query_string={'index': item_id})
    assert response.json == correct_response

    incomplete_skill = {
        "name": "JavaScript",
        "logo": "example-logo.png"
    }

    response = app.test_client().post('/resume/skill', json=incomplete_skill)
    assert response.status_code == 400
    assert "Missing fields" in response.json['error']

    invalid_skill = {
        "name": "JavaScript",
        "proficiency": 123,  # not a string
        "logo": "example-logo.png"
    }

    response = app.test_client().post('/resume/skill', json=invalid_skill)
    assert response.status_code == 400
    assert "Some fields have incorrect type" in response.json['error']

def test_editing_existing_experience():
    '''
    Add a new experience
    Update this experience by passing full new experience object
    Check that it returns the updated experience
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cool Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing Python Code",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']
    updated_experience = {
        "title": "Mechanical Engineer",
        "company": "Not A Cool Company",
        "start_date": "January 2022",
        "end_date": "Present",
        "description": "Maintanence Engineer",
        "logo": "example-logo2.png"
    }
    response = app.test_client().put(f'/resume/experience?index={item_id}', json=updated_experience)
    assert response.json == updated_experience

def test_editing_existing_experience_partially():
    '''
    Add a new experience
    Update this experience by passing just field to be update
    Check that it returns the updated experience
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cool Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing Python Code",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']
    field_to_be_updated = {
        "company": "Not A Cool Company",
    }
    response = app.test_client().put(f'/resume/experience?index={item_id}',
                                     json=field_to_be_updated)
    full_updated_experience = {
        "title": "Software Developer",
        "company": "Not A Cool Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing Python Code",
        "logo": "example-logo.png"
    }
    assert response.json == full_updated_experience
