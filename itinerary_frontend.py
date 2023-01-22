from typing import Callable

from itinerary_backend import ItineraryGenerator


def print_itinerary(itinerary_dict: dict[str, dict[str, list[str]]]):
    for location, activity_type in itinerary_dict.items():
        print(location + ":\n")

        for types, activities_list in activity_type.items():
            print(types + ":")
            for activity in activities_list:
                print(activity)
            print()
        print()

class ItineraryFrontend:
    _WELCOME_MSG = "Choose a number from the following menu:\n" \
                   "1. Add a location to the system\n" \
                   "2. Add an activity type to the system\n" \
                   "3. Add an attraction to the system\n" \
                   "4. Add a question to the system\n" \
                   "5. Build an itinerary for a group\n\n"
    _WELCOME_ERROR = "Error, you did not select a valid number\n"
    _QUESTION_ERROR = "Error, you already have this question in the system\n\n"
    _ADD_QUESTION_MSG = "Type the equivalent yes/no question (geared " \
                              "towards an attraction) you would like to add " \
                              "to the system:\n\n"
    _ADD_GROUP_QUESTION_MSG = "Type a yes/no question (geared towards a " \
                             "group) " \
                          "you " \
                        "would like to add to the system:\n\n"
    _ATTRACTION_ERROR = "Error, you already have this attraction in the " \
                        "system\n\n"
    _ADD_ATTRACTION_MSG = "Type an attraction you would like to add to the " \
                          "system:\n\n"
    _ACTIVITY_TYPE_ERROR = "Error, you already have this activity type in " \
                           "the system\n\n "
    _ADD_ACTIVITY_TYPE_MSG = "Type an activity type you would like to add to " \
                             "the system:\n\n"
    _LOCATION_ERROR = "Error, you already have this location in the system\n\n"
    _ADD_LOCATION_MSG = "Type a location you would like to add to the " \
                       "system:\n\n"
    _ANSWER_PROMPT = "Select a number:\n 1. Yes\n 0. No\n\n"
    _ANSWER_ERROR = "Error, you didn't select a valid number. Try again.\n\n"
    _ANSWER_MULT_ERROR = "Error, you didn't select a valid option. Try " \
                        "again.\n\n"
    _ANSWER_MULT_PROMPT = "Type an option from the list above.\n\n"
    _LOCATION_SUCCESS = "Location added successfully.\n\n"
    _ACTIVITY_SUCCESS = "Activity type added successfully.\n\n"
    _QUESTIONS_SUCCESS = "Questions added successfully.\n\n"
    _ATTRACTION_SUCCESS = "Attraction added successfully.\n\n"

    def __init__(self, generator: ItineraryGenerator):
        self._itinerary_generator = generator

    def run(self):
        while True:
            selection: str = input(self._WELCOME_MSG)
            if selection.isdigit() and 0 < int(selection) < 6:
                break
            else:
                print(self._WELCOME_ERROR)
        match int(selection):
            case 1:
                self.add_location()
            case 2:
                self.remove_location()
            case 3:
                self.add_activity_type()
            case 4:
                self.add_attraction()
            case 5:
                self.add_question()
            case 6:
                self.create_itinerary()

    def create_itinerary(self):
        print_itinerary(self._itinerary_generator.get_itinerary(
            self._ask_group_questions()))

    def add_question(self):
        question: str = input(self._ADD_QUESTION_MSG)
        group_question: str = input(self._ADD_GROUP_QUESTION_MSG)
        if self._itinerary_generator.is_attraction_question_valid(
                question, group_question):
            answers: dict[str, str] = self._get_question_answers(
                question)
            self._itinerary_generator.add_attraction_question(
                question, group_question, answers)
            print(self._QUESTIONS_SUCCESS)
        else:
            print(self._QUESTION_ERROR)

    def add_attraction(self):
        attraction: str = input(self._ADD_ATTRACTION_MSG)
        if self._itinerary_generator.is_attraction_valid(
                attraction):
            answers: dict[str, str] = self._get_attraction_answers(
                attraction)
            self._itinerary_generator.add_attraction(attraction,
                                                     answers)
            print(self._ATTRACTION_SUCCESS)
        else:
            print(self._ATTRACTION_ERROR)

    def add_activity_type(self):
        if self._itinerary_generator.add_activity_type(input(
                self._ADD_ACTIVITY_TYPE_MSG)):
            print(self._ACTIVITY_SUCCESS)
        else:
            print(self._ACTIVITY_TYPE_ERROR)

    def add_location(self):
        if self._itinerary_generator.add_location(input(
                self._ADD_LOCATION_MSG)):
            print(self._LOCATION_SUCCESS)
        else:
            print(self._LOCATION_ERROR)

    def _ask_group_questions(self) -> str:
        questions: list[str] = self._itinerary_generator.get_group_questions()
        answer_code: str = ""
        for question in questions:
            while True:
                print(question)
                answer = input(self._ANSWER_PROMPT)
                if answer == "0" or answer == "1":
                    break
                print(self._ANSWER_ERROR)
            answer_code += answer
        return answer_code

    def _get_attraction_answers(self, attraction: str) -> dict[str, str]:
        questions: list[str] = itinerary_generator.get_attraction_questions()
        default_q_a: list[list[str], list[
            str]] = itinerary_generator.get_default_attraction_questions_answers()
        default_q: list[str] = default_q_a[0]
        default_a: list[str] = default_q_a[1]
        answers: dict[str, str] = {}
        for i in range(len(default_q)):
            while True:
                print(attraction)
                print(default_q[i])
                print(default_a[i])
                temp_answer = input(self._ANSWER_MULT_PROMPT)
                if temp_answer in default_a[i]:
                     break
                print(self._ANSWER_ERROR)
            answers[default_q[i]]: str = temp_answer
        for question in questions:
            while True:
                print(attraction)
                print(question)
                temp_answer = input(self._ANSWER_PROMPT)
                if temp_answer == "0" or temp_answer == "1":
                    break
                print(self._ANSWER_ERROR)
            answers[question]: str = temp_answer
        return answers

    def _get_question_answers(self, question: str) -> dict[str, str]:
        attractions: list[str] = itinerary_generator.get_attractions()
        answers: dict = {}
        for attraction in attractions:
            while True:
                print(attraction)
                print(question)
                temp_answer = input(self._ANSWER_PROMPT)
                if temp_answer == "0" or temp_answer == "1":
                    break
                print(self._ANSWER_ERROR)
            answers[attraction]: str = temp_answer
        return answers

    def remove_location(self):
        if self._itinerary_generator.remove_location(input(
                self._REMOVE_LOCATION_MSG)):
            print(self._LOCATION_SUCCESS)
        else:
            print(self._LOCATION_ERROR)


if __name__ == '__main__':
    itinerary_generator = ItineraryGenerator(
        input_stream="./itinerarygenerator.json")
    itinerary = ItineraryFrontend(itinerary_generator)
    while True:
        itinerary.run()
