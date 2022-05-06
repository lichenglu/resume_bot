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

        if not equation:
            dispatcher.utter_message(text="It seems that you did not put a valid equation. I would recommend using the equation calculator to type it. Or at lease put the equation BETWEEN TWO dollar signs ($)")
            return []

        if help_seeking_mode == 'solve':
            dispatcher.utter_message(text=f"Solved: {equation}")
        elif help_seeking_mode == 'simplify':
            dispatcher.utter_message(text=f"Simplified: {equation}")

        return []


class ActionPlayRPS(Action):

    def name(self) -> Text:
        return "action_play_rps"

    def computer_choice(self):
        generatednum = random.randint(1,3)
        if generatednum == 1:
            computerchoice = "rock"
        elif generatednum == 2:
            computerchoice = "paper"
        elif generatednum == 3:
            computerchoice = "scissors"
       
        return(computerchoice)
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        # play rock paper scissors
        user_choice = tracker.get_slot("choice")
        dispatcher.utter_message(text=f"You chose {user_choice}")
        comp_choice = self.computer_choice()
        dispatcher.utter_message(text=f"The computer chose {comp_choice}")
 
        if user_choice == "rock" and comp_choice == "scissors":
            dispatcher.utter_message(text="Congrats, you won!")
        elif user_choice == "rock" and comp_choice == "paper":
            dispatcher.utter_message(text="The computer won this round.")
        elif user_choice == "paper" and comp_choice == "rock":
            dispatcher.utter_message(text="Congrats, you won!")
        elif user_choice == "paper" and comp_choice == "scissors":
            dispatcher.utter_message(text="The computer won this round.")
        elif user_choice == "scissors" and comp_choice == "paper":
            dispatcher.utter_message(text="Congrats, you won!")
        elif user_choice == "scissors" and comp_choice == "rock":
            dispatcher.utter_message(text="The computer won this round.")
        else:
            dispatcher.utter_message(text="It was a tie!")
 
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
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        print("extract_equation triggered")
        try:
            text_of_last_user_message = tracker.latest_message.get("text")
            pat = r'.*?\$(.*)\$.*'

            if match := re.search(pat, text_of_last_user_message):
                return {"equation": match.group(1)}
            else:
                return {"equation": None}
        except:
            dispatcher.utter_message(text=f"Oops...I didn't get it")
            return {"equation": None}