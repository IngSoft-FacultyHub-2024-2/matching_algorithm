import unittest
import copy 

from src.matching_algorithm.quality_assurance import validate_unassigned_classes
from src.matching_algorithm import Assignments, ConflictModel
from .util import convert_teachers_and_classes_dict_to_model
import unittest

# Example data for tests
teachers = { 
    'teacher1': {
        "seniority": 2,
        'subject_he_know_how_to_teach': [{'subject': 'Math', 'role': ['Theory']}],
        'available_times': {'Monday': [9, 10], 'Tuesday': [9, 10]},
        'weekly_hours_max_work': 10
    },
    'teacher2': {
        "seniority": 2,
        'subject_he_know_how_to_teach': [{'subject': 'Math', 'role': ['Theory']}],
        'available_times': {'Monday': [9, 10], 'Tuesday': [9, 10], 'Wednesday': [9, 10]},
        'weekly_hours_max_work': 8
    },
    'teacher3': {
        "seniority": 2,
        'subject_he_know_how_to_teach': [{'subject': 'Science', 'role': ['Practice']}],
        'available_times': {'Monday': [9, 10], 'Wednesday': [10]},
        'weekly_hours_max_work': 5
    }
}

classes = { 
    'class1': {
        'subject': 'Math',
        'subClasses': [{'role': 'Theory', 'times': {'Monday': [9], 'Tuesday': [9]}, 'num_teachers': 1}]
    },
    'class2': {
        'subject': 'Math',
        'subClasses': [{'role': 'Theory', 'times': {'Monday': [10], 'Wednesday': [10]}, 'num_teachers': 2}]
    },
    'class3': {
        'subject': 'Science',
        'subClasses': [{'role': 'Practice', 'times': {'Monday': [9]}, 'num_teachers': 1}]
    }
}

result = { 
    'class1': {'Theory': ['teacher1']},
    'class2': {'Theory': []},
    'class3': {'Practice': ['teacher3']}
}

unassigned = [('class2', 'Theory')]

class TestValidateUnassignedClasses(unittest.TestCase):

    def test_completely_unassigned_classes(self):
        assignments = Assignments(copy.deepcopy(result), copy.deepcopy(unassigned), ConflictModel()) 
        teachers_dict, classes_dict = convert_teachers_and_classes_dict_to_model(teachers, classes)
        validation_issues = validate_unassigned_classes(teachers_dict, classes_dict, assignments)
        self.assertEqual(len(validation_issues), 1)
        issue = validation_issues[0]
        self.assertEqual(issue['class_name'], 'class2')
        self.assertEqual(issue['role'], 'Theory')
        self.assertEqual(issue['type'], 'completely_unassigned')
        self.assertEqual(issue['teachers_needed'], 2)
        self.assertEqual(len(issue['potential_teachers']), 1)
        self.assertEqual(issue['potential_teachers'][0]["teacher"], 'teacher2')

    def test_not_partially_unassigned_classes(self):
        assignments = Assignments(copy.deepcopy(result), copy.deepcopy(unassigned), ConflictModel()) 
        assignments.matches['class2']['Theory'] = ['teacher2']
        teachers_dict, classes_dict = convert_teachers_and_classes_dict_to_model(teachers, classes)
        validation_issues = validate_unassigned_classes(teachers_dict, classes_dict, assignments)
        self.assertEqual(len(validation_issues), 0)

    def test_partially_unassigned_classes(self):
        result['class2']['Theory'] = ['teacher2']
        teachers['teacher4'] = teachers['teacher2'].copy()
        partially_unassigned = [{'class_name': 'class2', 'role': 'Theory', 'assigned': 1, 'needed': 2}]
        assignments = Assignments(copy.deepcopy(result), [], ConflictModel(partially_unassigned=partially_unassigned)) 
        teachers_dict, classes_dict = convert_teachers_and_classes_dict_to_model(teachers, classes)
        validation_issues = validate_unassigned_classes(teachers_dict, classes_dict, assignments)
        self.assertEqual(len(validation_issues), 1)
        issue = validation_issues[0]
        self.assertEqual(issue['class_name'], 'class2')
        self.assertEqual(issue['role'], 'Theory')
        self.assertEqual(issue['type'], 'partially_unassigned')
        self.assertEqual(issue['teachers_assigned'], 1)
        self.assertEqual(issue['teachers_needed'], 2)
        self.assertEqual(len(issue['potential_teachers']), 1)
        self.assertEqual(issue['potential_teachers'][0]["teacher"], 'teacher4')
    
    def test_no_issues_all_classes_assigned(self):
        classes['class2']['subClasses'][0]['num_teachers'] = 1
        result['class2']['Theory'] = ['teacher2']
        assignments = Assignments(copy.deepcopy(result), [], ConflictModel()) 
        teachers_dict, classes_dict = convert_teachers_and_classes_dict_to_model(teachers, classes)
        validation_issues = validate_unassigned_classes(teachers_dict, classes_dict, assignments)
        self.assertEqual(len(validation_issues), 0)

    def test_no_issues_no_one_can_teach_because_subject_he_know(self):
        teachers_without_teacher2 = copy.deepcopy(teachers)
        del teachers_without_teacher2['teacher2']
        assignments = Assignments(copy.deepcopy(result), [], ConflictModel()) 
        teachers_without_teacher2, classes_dict = convert_teachers_and_classes_dict_to_model(teachers_without_teacher2, classes)
        validation_issues = validate_unassigned_classes(teachers_without_teacher2, classes_dict, assignments)       
        self.assertEqual(len(validation_issues), 0)

    def test_no_issues_no_one_can_teach_because_amount_of_hours(self):
        teachers_without_teacher2 = copy.deepcopy(teachers)
        del teachers_without_teacher2['teacher2']    
        teachers_without_teacher2['teacher3']['subject_he_know_how_to_teach'].append({'subject': 'Math', 'role': ['Theory']})
        teachers_without_teacher2['teacher3']['weekly_hours_max_work'] = 2
        assignments = Assignments(copy.deepcopy(result), [], ConflictModel()) 
        teachers_without_teacher2, classes_dict = convert_teachers_and_classes_dict_to_model(teachers_without_teacher2, classes)
        validation_issues = validate_unassigned_classes(teachers_without_teacher2, classes_dict, assignments)     
        self.assertEqual(len(validation_issues), 0)



if __name__ == '__main__':
    unittest.main()
