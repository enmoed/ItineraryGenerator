import json
from typing import Union



class ItineraryGenerator:
    _ANSWER_CODE = "Code"
    _GROUP_QUESTIONS = "Group Questions"
    _ITINERARY_QUESTIONS = "Itinerary Questions"
    _ATTRACTIONS = "Attractions"
    _WHAT_ATTRACTION_TYPE = "What type of attraction is this?"
    _WHAT_LOCATION = "What is the location of this activity?"
    _ACTIVITIES = "Activity Types"
    _LOCATIONS = "Locations"

    def __init__(self, input_stream=None):
        _itinerary_dict: dict = {}
        self._input_stream = input_stream
        self._attractions: dict[str, dict[str, str]] = {}
        self._group_questions: list[str] = []
        self._attraction_questions: list[str] = []
        self._activity_types: list[str] = []
        self._locations: list[str] = []
        if input_stream is not None:
            itineraries = open(input_stream, "r")
            _itinerary_dict: dict[str, Union[list[str], dict[str,
                                                             dict[
                                                                 str,
                                                                 str]]]] = \
                json.load(
                itineraries)
            itineraries.close()
        if self._ATTRACTIONS in _itinerary_dict:
            self._attractions = _itinerary_dict.pop(self._ATTRACTIONS)
        if self._GROUP_QUESTIONS in _itinerary_dict:
            self._group_questions = _itinerary_dict.pop(self._GROUP_QUESTIONS)
        if self._ITINERARY_QUESTIONS in _itinerary_dict:
            self._attraction_questions = _itinerary_dict.pop(
                self._ITINERARY_QUESTIONS)
        if self._ACTIVITIES in _itinerary_dict:
            self._activity_types = _itinerary_dict.pop(self._ACTIVITIES)
        if self._LOCATIONS in _itinerary_dict:
            self._locations = _itinerary_dict.pop(self._LOCATIONS)

    def is_attraction_question_valid(self, question: str, group_question) -> bool:
        for dic_questions in self._attraction_questions:
            if question.lower().replace(" ", "").strip("?") == \
                    dic_questions.replace(" ", "").strip("?"):
                return False
        for dic_questions in self._group_questions:
            if group_question.lower().replace(" ", "").strip("?") == \
                    dic_questions.replace(" ", "").strip("?"):
                return False
        for default_question in self._get_attraction_sorting_questions():
            if default_question.lower().replace(" ", "").strip("?") == \
                    group_question.lower().replace(" ", "").strip("?") or \
                    default_question.lower().replace(" ", "").strip("?") == \
                    question.lower().replace(" ", "").strip("?"):
                return False
        return True

    def add_attraction_question(self, attraction_question: str,
                                group_question: str,
                                answers: dict[str,str]) -> bool:
        self._add_attraction_question(attraction_question, group_question,
                                      answers)
        self._save()
        return True

    def _add_attraction_question(self, question: str, group_question: str,
                                 answers: dict[str,  str]) -> None:
        self._group_questions.append(group_question)
        self._attraction_questions.append(question)
        for attraction in self._attractions.keys():
            self._attractions[attraction][question] = answers[attraction]
            self._attractions[attraction][self._ANSWER_CODE] += answers[
                attraction]

    def get_attractions(self) -> list[str]:
        return list(self._attractions.keys())

    def _is_activity_type_valid(self, new_activity_type: str) -> bool:
        for activity_type in self._activity_types:
            if activity_type.capitalize().replace(" ", "") == \
                    new_activity_type.capitalize().replace(" ", ""):
                return False
        return True

    def add_activity_type(self, new_activity_type: str) -> bool:
        if not self._is_activity_type_valid(new_activity_type):
            return False
        self._activity_types.append(new_activity_type.capitalize())
        self._save()
        return True

    def _is_location_valid(self, location: str) -> bool:
        for inserted_location in self._locations:
            if inserted_location.capitalize().replace(" ", "") == \
                    location.capitalize().replace(" ", ""):
                return False
        return True

    def add_location(self, location: str) -> bool:
        if not self._is_location_valid(location):
            return False
        self._locations.append(location.capitalize())
        self._save()
        return True

    def is_attraction_valid(self, new_attraction: str) -> bool:
        for attraction in self._attractions.keys():
            if new_attraction.lower().replace(" ", "") == attraction.lower(
            ).replace(" ", ""):
                return False
        return True

    def add_attraction(self, new_attraction: str, answers: dict[str, str]) -> \
            bool:
        self._add_attraction(new_attraction, answers)
        self._save()
        return True

    def _add_attraction(self, new_attraction: str, answers: dict[str, str]) -> None:
        code = ""
        for question in self._attraction_questions:
            code += answers[question]
        answers[self._ANSWER_CODE] = code
        self._attractions[new_attraction] = answers

    def get_default_attraction_questions_answers(self) -> list[list[str]]:
        default_questions: list[str] = [self._WHAT_ATTRACTION_TYPE, self._WHAT_LOCATION]
        default_answers: list[list] = [self._activity_types, self._locations]
        return [default_questions, default_answers]

    def get_attraction_questions(self) -> list[str]:
        return self._attraction_questions

    def get_group_questions(self) -> list[str]:
        return self._group_questions

    def get_itinerary(self, code: str) -> dict[str, dict[str, list[str]]]:
        itinerary: dict[str, dict[str, list[str]]] = {}
        for location in self._locations:
            itinerary[location]: dict = {}
            for activity in self._activity_types:
                itinerary[location][activity] = []
        for attraction, questions in self._attractions.items():
            if (int(code, 2) & int(questions[self._ANSWER_CODE], 2)) == int(
                    code, 2):
                itinerary[questions[self._WHAT_LOCATION]][questions[
                    self._WHAT_ATTRACTION_TYPE]].append(attraction)
        return itinerary

    def _get_attraction_sorting_questions(self) -> list[str]:
        return [self._WHAT_ATTRACTION_TYPE, self._WHAT_LOCATION]

    def _save(self):
        _itinerary_dict = {self._ATTRACTIONS: self._attractions,
                           self._GROUP_QUESTIONS: self._group_questions,
                           self._ITINERARY_QUESTIONS: self._attraction_questions,
                           self._ACTIVITIES: self._activity_types,
                           self._LOCATIONS: self._locations}
        with open(self._input_stream, 'w') as outfile:
            json.dump(_itinerary_dict, outfile)

    def remove_location(self, location: str) -> None:
        if self._is_location_valid(location):
            # TODO: error
            return
        
