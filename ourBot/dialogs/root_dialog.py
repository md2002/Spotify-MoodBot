# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict
from recognizers_text import Culture

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    NumberPrompt,
    PromptValidatorContext,
)
from botbuilder.dialogs.prompts import TextPrompt
from botbuilder.core import MessageFactory, UserState

from dialogs import SlotFillingDialog
from dialogs.slot_details import SlotDetails


class RootDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(RootDialog, self).__init__(RootDialog.__name__)

        self.user_state_accessor = user_state.create_property("result")

        # Rather than explicitly coding a Waterfall we have only to declare what properties we want collected.
        # In this example we will want two text prompts to run, one for the first name and one for the last
        fullname_slots = [
            SlotDetails(
                name="first", dialog_id="text", prompt="Please enter your first name."
            ),
            SlotDetails(
                name="last", dialog_id="text", prompt="Please enter your last name."
            ),
        ]

        # This defines an era dialog that collects  genre and favartists properties.
        era_slots = [
            SlotDetails(
                name="era",
                dialog_id="text",
                prompt="What is your preferred era of music?",
            ),
            SlotDetails(name="genre", dialog_id="text", prompt="What Genre do you like the best?"),
            SlotDetails(name="favartists", dialog_id="text", prompt="Any favorite artists?"),
        ]

        # Dialogs can be nested and the slot filling dialog makes use of that. In this example some of the child
        # dialogs are slot filling dialogs themselves.
        slots = [
            SlotDetails(name="fullname", dialog_id="fullname",),
            SlotDetails(
                name="age", dialog_id="number", prompt="Please enter your age."
            ),
            SlotDetails(
                name="feel",
                dialog_id="text",
                prompt="How are you feeling today?",
                retry_prompt="Be as specific as you can be! We will use this information to suggest songs that best suit your mood :)",
            ),
            SlotDetails(name="era", dialog_id="era"),
        ]

        # Add the various dialogs that will be used to the DialogSet.
        self.add_dialog(SlotFillingDialog("era", era_slots))
        self.add_dialog(SlotFillingDialog("fullname", fullname_slots))
        self.add_dialog(SlotFillingDialog("feel",slots))
        self.add_dialog(TextPrompt("text"))
        self.add_dialog(NumberPrompt("number", default_locale=Culture.English))
        
        
        self.add_dialog(SlotFillingDialog("slot-dialog", slots))

        # Defines a simple two step Waterfall to test the slot dialog.
        self.add_dialog(
            WaterfallDialog("waterfall", [self.start_dialog, self.process_result])
        )

        # The initial child Dialog to run.
        self.initial_dialog_id = "waterfall"

    async def start_dialog(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Start the child dialog. This will run the top slot dialog than will complete when all the properties are
        # gathered.
        return await step_context.begin_dialog("slot-dialog")

    async def process_result(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # To demonstrate that the slot dialog collected all the properties we will echo them back to the user.
        if isinstance(step_context.result, dict) and len(step_context.result) > 0:
            fullname: Dict[str, object] = step_context.result["fullname"]
            feeling: float = step_context.result["feel"]
            era: dict = step_context.result["era"]

            # store the response on UserState
            obj: dict = await self.user_state_accessor.get(step_context.context, dict)
            obj["data"] = {}
            obj["data"]["fullname"] = f"{fullname.get('first')} {fullname.get('last')}"
            obj["data"]["feel"] = f"{feeling}"
            obj["data"][
                "era"
            ] = f"{era['era']}, {era['genre']}, {era['favartists']}"

            # show user the values
            await step_context.context.send_activity(
                MessageFactory.text(obj["data"]["fullname"])
            )
            await step_context.context.send_activity(
                MessageFactory.text(obj["data"]["feel"])
            )
            await step_context.context.send_activity(
                MessageFactory.text(obj["data"]["era"])
            )
            #change1 
            with open('info.txt', 'w') as f:
                f.write(f"{fullname.get('first')} {fullname.get('last')}, {feeling}, {era['era']}, {era['genre']}, {era['favartists']}")

        return await step_context.end_dialog()

    # @staticmethod
    # async def feeling_validator(prompt_context: PromptValidatorContext) -> bool:
    #     if not prompt_context.recognized.value:
    #         return False

    #     feeling = round(prompt_context.recognized.value, 1)

    #     # show sizes can range from 0 to 16, whole or half sizes only
    #     if 0 <= feeling <= 16 and (feeling * 2) % 1 == 0:
    #         prompt_context.recognized.value = feeling
    #         return True
    #     return False
