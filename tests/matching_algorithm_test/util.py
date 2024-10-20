from src.matching_algorithm import ClassModel, TeacherModel


def convert_teachers_and_classes_dict_to_model(
    teachers: dict, classes: dict
) -> tuple[dict[str, TeacherModel], dict[str, ClassModel]]:
    teachers = convert_teachers_model_to_dict(teachers)
    classes = convert_classes_model_to_dict(classes)
    return teachers, classes


def convert_teachers_model_to_dict(teachers: dict[str, dict]) -> dict[str, TeacherModel]:
    return {k: TeacherModel(**v) for k, v in teachers.items()}


def convert_classes_model_to_dict(classes: dict[str, dict]) -> dict[str, ClassModel]:
    return {k: ClassModel(**v) for k, v in classes.items()}
