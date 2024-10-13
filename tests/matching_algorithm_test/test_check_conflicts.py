import unittest

from src.matching_algorithm.quality_assurance.check_conflicts import are_conflicts

class TestCheckConflicts(unittest.TestCase):

    def setUp(self):
        self.teachers = {
            "teacher1": {
                "subject_he_know_how_to_teach": [{"subject": "Math", "role": "Theory"}],
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
                    {"role": "Theory", "times": {"Monday": [9], "Tuesday": [9]}}
                ]
            },
            "class2": {
                "subject": "Math",
                "subClasses": [
                    {"role": "Theory", "times": {"Monday": [9]}}
                ]
            }
        }
        self.assignment = {
            "class1": {
                "Theory": ["teacher1"]
            }
        }

    def test_no_conflicts(self):
        self.assertFalse(are_conflicts(self.assignment, self.teachers, self.classes))

    def test_teacher_cannot_teach_class_because_of_knowledge(self):
        self.teachers["teacher1"]["subject_he_know_how_to_teach"] = []
        self.assertTrue(are_conflicts(self.assignment, self.teachers, self.classes))
    
    def test_teacher_cannot_teach_class_because_of_role(self):
        self.teachers["teacher1"]["subject_he_know_how_to_teach"][0]["role"] = "Practice"
        self.assertTrue(are_conflicts(self.assignment, self.teachers, self.classes))

    def test_teacher_has_more_than_weekly_hours(self):
        self.teachers["teacher1"]["weekly_hours_max_work"] = 1
        self.assertTrue(are_conflicts(self.assignment, self.teachers, self.classes))

    def test_teacher_teach_more_than_one_class_at_same_time(self):
        self.assignment["class2"] = {"Theory": ["teacher1"]}
        self.assertTrue(are_conflicts(self.assignment, self.teachers, self.classes))

if __name__ == '__main__':
    unittest.main()