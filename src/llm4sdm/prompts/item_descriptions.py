"""Descriptions of the OPTION items and their scoring criteria.

Source:
https://doi.org/10.1016/j.pec.2015.12.019.
(https://www.sciencedirect.com/science/article/pii/S0738399115301725)
"""

OPTION_ITEMS = [
    # 1
    {
        "description": "The clinician draws attention to an identified problem as one that requires a decision making process.",
        "scoring": {
            0: "not observed",
            1: "short problem definition",
            2: "attention the problem, baseline skill",
            3: "attention the problem, decision should be made",
            4: "need for a decision",
        },
    },
    # 2
    {
        "description": "The clinician states that there is more than one way to deal with the identified problem ('equipoise').",
        "scoring": {
            0: "no options mentioned",
            1: "listing the options",
            2: "little explanation of the options",
            3: "explaining pros and cons of all options",
            4: "both options are o.k., depends on the preferences of the patient",
        },
    },
    # 3
    {
        "description": "The clinician assesses the patient's preferred approach to receiving information to assist decision making (e.g. discussion, reading printed material, assessing graphical data, using videotapes or other media).",
        "scoring": {
            0: "no information",
            1: "short (do you want a brochure?)",
            2: "how do you like to receive the information",
            3: "several options are possible to receive information",
            4: "listing examples how to receive information and ask the preferences of the patient",
        },
    },
    # 4
    {
        "description": "The clinician lists 'options', which can include the choice of 'no action'.",
        "scoring": {
            0: "no options mentioned",
            1: "listing the options",
            2: "little explanation of the options (you can choose ... or ...)",
            3: "extensively listing options (no action is a possibility)",
            4: "very detailed explanation of all options",
        },
    },
    # 5
    {
        "description": "The clinician explains the pros and cons of options to the patient (taking 'no action' is an option).",
        "scoring": {
            0: "no explanation",
            1: "explaining pros and cons of some options",
            2: "explaining pros and cons of all options",
            3: "explaining pros and cons of all options including the little pros and cons",
            4: "very detailed explanation of the pros and cons of all options",
        },
    },
    # 6
    {
        "description": "The clinician explores the patient's expectations (or ideas) about how the problem(s) are to be managed.",
        "scoring": {
            0: "not observed",
            1: "asking the expectations in passing",
            2: "asking the expectations (only asking)",
            3: "asking the expectations",
            4: "asking the expectations, high standard (discussing the expectations)",
        },
    },
    # 7
    {
        "description": "The clinician explores the patient’s concerns (fears) about how problem(s) are to be managed.",
        "scoring": {
            0: "not observed",
            1: "asking about the concerns (in passing)",
            2: "asking about the concerns (only asking)",
            3: "asking about the concerns",
            4: "asking about the concerns, high standard (discussing the concerns)",
        },
    },
    # 8
    {
        "description": "The clinician checks that the patient has understood the information",
        "scoring": {
            0: "not observed",
            1: "listing the options",
            2: "is it clear (you can ask questions)",
            3: "checking if it is clear by asking the patient to repeat the information",
            4: "high standard",
        },
    },
    # 9
    {
        "description": "The clinician offers the patient explicit opportunities to ask questions during the decision making process.",
        "scoring": {
            0: "not observed",
            1: "breaks or interruptions",
            2: "possibility to ask questions (Do you have any questions)",
            3: "any questions about the options or treatments?",
            4: "any questions about the options or treatments? High standard",
        },
    },
    # 10
    {
        "description": "The clinician elicits the patient’s preferred level of involvement in decision-making.",
        "scoring": {
            0: "not observed",
            1: "short asking",
            2: "asking explicit (do you want to be involved in decision making?)",
            3: "information about the possible options in involvement",
            4: "easy to understand for the patient",
        },
    },
    # 11
    {
        "description": "The clinician indicates the need for a decision making (or deferring) stage.",
        "scoring": {
            0: "no indication",
            1: "decision should be made",
            2: "indicates need for decision",
            3: "indicates need for decision, good standard",
            4: "indicates need for decision, high standard",
        },
    },
    # 12
    {
        "description": "The clinician indicates the need to review the decision (or deferment).",
        "scoring": {
            0: "not observed",
            1: "short (follow-up appointment)",
            2: "follow-up appointment, possible to return the decision",
            3: "appointment for evaluating the decision, good standard",
            4: "appointment for evaluating the decision, high standard (explicit)",
        },
    },
]
