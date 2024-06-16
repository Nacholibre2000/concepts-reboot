from flask import Blueprint, jsonify
from .models import Schools, Subjects, Grades, Subsections, Central_contents, Central_requirements 

views = Blueprint('views', __name__)

def fetch_related_items(table_name, item_id):
    #print(f"Fetching related items for table: {table_name}, ID: {item_id}")  # Debugging line
    children = []
    if table_name == 'Schools':
        related_subjects = Subjects.query.filter_by(foreign_id_school=item_id).all()
        for subject in related_subjects:
            subject_dict = subject.serialize()
            subject_dict['children'] = fetch_related_items('Subjects', subject.id)
            children.append(subject_dict)
    elif table_name == 'Subjects':
        related_grades = Grades.query.filter_by(foreign_id_subject=item_id).all()
        for grade in related_grades:
            grade_dict = grade.serialize()
            grade_dict['children'] = fetch_related_items('Grades', grade.id)
            children.append(grade_dict)
    elif table_name == 'Grades':
        related_subsections = Subsections.query.filter_by(foreign_id_grade=item_id).all()
        related_central_requirements = Central_requirements.query.filter_by(foreign_id_grade=item_id).all()
        for subsection in related_subsections:
            subsection_dict = subsection.serialize()
            subsection_dict['children'] = fetch_related_items('Subsections', subsection.id)
            children.append(subsection_dict)
        for central_requirement in related_central_requirements:
            children.append(central_requirement.serialize())
    elif table_name == 'Subsections':
        related_central_contents = Central_contents.query.filter_by(foreign_id_subsection=item_id).all()
        for central_content in related_central_contents:
            children.append(central_content.serialize())
    return children

@views.route('/api/sidebar-data', methods=['GET'])

def get_sidebar_data():
    print("Fetching initial sidebar data...")  # Debugging line
    schools = Schools.query.all()
    school_data = []
    for school in schools:
        print(f"Processing school: {school}")  # Debugging line
        school_dict = school.serialize()
        school_dict['children'] = fetch_related_items('Schools', school.id)
        school_data.append(school_dict)
    #print(f"Final sidebar data: {school_data}")  # Debugging line
    #print("JSON Response:", jsonify(school_data).get_json())  # Add this line
    return jsonify(school_data)