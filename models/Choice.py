from collections import Callable


class Choice:
    def __init__(self, choice_id: str, text: str, callback: Callable):
        self.id = choice_id
        self.text = text
        self.callback = callback

    def chosen(self):
        self.callback()


class ChoiceNode:
    def __init__(self, choice_node_id: str, question: str, choices: list[Choice]):
        self.id = choice_node_id
        self.question = question
        self.choices = choices
