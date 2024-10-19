import unittest

from src.matching_algorithm.quality_assurance import are_conflicts
from .util import convert_teachers_and_classes_dict_to_model

class TestCheckConflicts(unittest.TestCase):

    def setUp(self):
        self.teachers = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [{"subject": "Math", "role": ["Theory"]}],
                "available_times": {
                    "Monday": [9, 10],
                    "Tuesday": [9, 10]
                },
                "weekly_hours_max_work": 10
            }
        }
        self.classes = {
            "class1": {
                "subject": "Math",
                "subClasses": [
                    {"role": "Theory", "times": {"Monday": [9], "Tuesday": [9]}, "num_teachers": 1}
                ]
            },
            "class2": {
                "subject": "Math",
                "subClasses": [
                    {"role": "Theory", "times": {"Monday": [9]}, "num_teachers": 1}
                ]
            }
        }
        self.assignment = {
            "class1": {
                "Theory": ["teacher1"]
            }
        }

    def test_no_conflicts(self):
        teachers, classes = convert_teachers_and_classes_dict_to_model(self.teachers, self.classes)
        self.assertFalse(are_conflicts(self.assignment, teachers, classes))

    def test_teacher_cannot_teach_class_because_of_knowledge(self):
        self.teachers["teacher1"]["subject_he_know_how_to_teach"] = []
        teachers, classes = convert_teachers_and_classes_dict_to_model(self.teachers, self.classes)
        self.assertTrue(are_conflicts(self.assignment, teachers, classes))
    
    def test_teacher_cannot_teach_class_because_of_role(self):
        self.teachers["teacher1"]["subject_he_know_how_to_teach"][0]["role"] = ["Practice"]
        teachers, classes = convert_teachers_and_classes_dict_to_model(self.teachers, self.classes)
        self.assertTrue(are_conflicts(self.assignment, teachers, classes))

    def test_teacher_has_more_than_weekly_hours(self):
        self.teachers["teacher1"]["weekly_hours_max_work"] = 1
        teachers, classes = convert_teachers_and_classes_dict_to_model(self.teachers, self.classes)
        self.assertTrue(are_conflicts(self.assignment, teachers, classes))

    def test_teacher_teach_more_than_one_class_at_same_time(self):
        self.assignment["class2"] = {"Theory": ["teacher1"]}
        teachers, classes = convert_teachers_and_classes_dict_to_model(self.teachers, self.classes)
        self.assertTrue(are_conflicts(self.assignment, teachers, classes))

if __name__ == '__main__':
    unittest.main()