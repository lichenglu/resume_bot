# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import re

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher

DomainDict = Dict[Text, Any]

class ActionResolveEquation(Action):

    def name(self) -> Text:
        return "action_resolve_equation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print(tracker)
        help_seeking_mode = tracker.slots.get('help_seeking_mode')
        equation = tracker.slots.get('equation')

        if help_seeking_mode == 'solve':
            dispatcher.utter_message(text=f"Solved: {equation}")
        elif help_seeking_mode == 'simplify':
            dispatcher.utter_message(text=f"Simplified: {equation}")

        return []


class ValidateMathForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_math_form"

    @staticmethod
    def supported_mode() -> List[Text]:
        """Database of supported cuisines"""

        return ["solve", 'simplify', 'recommendation']

    def validate_help_seeking_mode(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate help seeking mode value."""

        if slot_value.lower() in self.supported_mode():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"help_seeking_mode": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"help_seeking_mode": None}

    def extract_equation(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        text_of_last_user_message = tracker.latest_message.get("text")
        pat = r'.*?\$(.*)\$.*'

        if match := re.search(pat, text_of_last_user_message):
            return {"equation": match.group(1)}
        else:
            return {"equation": None}