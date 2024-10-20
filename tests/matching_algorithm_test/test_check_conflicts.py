import unittest

from src.matching_algorithm.models import RoleType
from src.matching_algorithm.quality_assurance import are_conflicts
from tests.matching_algorithm_test.util import \
    convert_teachers_and_classes_dict_to_model


class TestCheckConflicts(unittest.TestCase):

    def setUp(self) -> None:
        self.teachers = {
            "teacher1": {
                "seniority": 2,
                "subject_he_know_how_to_teach": [{"subject": "Math", "role": ["Theory"]}],
                "available_times": {"Monday": [9, 10], "Tuesday": [9, 10]},
                "weekly_hours_max_work": 10,
            }
        }
        self.classes = {
            "class1": {
                "subject": "Math",
                "subClasses": [
                    {"role": "Theory", "times": {"Monday": [9], "Tuesday": [9]}, "num_teachers": 1}
                ],
            },
            "class2": {
                "subject": "Math",
                "subClasses": [{"role": "Theory", "times": {"Monday": [9]}, "num_teachers": 1}],
            },
        }
        self.assignment: dict[str, dict[RoleType, list[str]]] = {"class1": {"Theory": ["teacher1"]}}

    def test_no_conflicts(self) -> None:
        teachers, classes = convert_teachers_and_classes_dict_to_model(self.teachers, self.classes)
        self.assertFalse(are_conflicts(self.assignment, teachers, classes))

    def test_teacher_cannot_teach_class_because_of_knowledge(self) -> None:
        self.teachers["teacher1"]["subject_he_know_how_to_teach"] = []
        teachers, classes = convert_teachers_and_classes_dict_to_model(self.teachers, self.classes)
        self.assertTrue(are_conflicts(self.assignment, teachers, classes))

    def test_teacher_cannot_teach_class_because_of_role(self) -> None:
        self.teachers["teacher1"]["subject_he_know_how_to_teach"][0]["role"] = ["Practice"]  # type: ignore
        teachers, classes = convert_teachers_and_classes_dict_to_model(self.teachers, self.classes)
        self.assertTrue(are_conflicts(self.assignment, teachers, classes))

    def test_teacher_has_more_than_weekly_hours(self) -> None:
        self.teachers["teacher1"]["weekly_hours_max_work"] = 1
        teachers, classes = convert_teachers_and_classes_dict_to_model(self.teachers, self.classes)
        self.assertTrue(are_conflicts(self.assignment, teachers, classes))

    def test_teacher_teach_more_than_one_class_at_same_time(self) -> None:
        self.assignment["class2"] = {"Theory": ["teacher1"]}
        teachers, classes = convert_teachers_and_classes_dict_to_model(self.teachers, self.classes)
        self.assertTrue(are_conflicts(self.assignment, teachers, classes))


if __name__ == "__main__":
    unittest.main()
