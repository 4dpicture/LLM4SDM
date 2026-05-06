"""
Few-shot examples for OPTION-12 item scoring.

Each example contains:
- transcript: brief Dutch doctor-patient excerpt
- evaluation: JSON-formatted evaluation matching the prompt's required schema

Examples are chosen to cover different score levels (0-4) so the LLM
sees the full anchor range for each item.

NOTE: These examples are syntheticly generated without any examples from the real data.
"""

EXAMPLE_ASSESSMENTS_SYNTHETIC = {
    # ---------------------------------------------------------------------
    # Item 1: Drawing attention to a problem requiring a decision
    # ---------------------------------------------------------------------
    1: [
        {
            "transcript": (
                "Dokter: Goedemorgen, gaat u zitten. Hoe gaat het met u?\n"
                "Patiënt: Redelijk, dokter, maar die pijn in mijn knie blijft.\n"
                "Dokter: Ja, dat heb ik in uw dossier gezien. Laten we eens kijken naar de uitslagen."
            ),
            "evaluation": (
                "{\n"
                '  "score": 0,\n'
                '  "evidence": "No relevant utterance",\n'
                '  "justification": "The clinician acknowledges the complaint but does not '
                'frame it as a problem requiring a decision-making process."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: De uitslag laat zien dat er sprake is van artrose in uw knie. "
                "We moeten samen bespreken wat we hieraan gaan doen, want er zijn "
                "verschillende mogelijkheden en de keuze hangt ook af van wat u zelf wilt.\n"
                "Patiënt: Oké, dat is goed."
            ),
            "evaluation": (
                "{\n"
                '  "score": 4,\n'
                '  "evidence": "We moeten samen bespreken wat we hieraan gaan doen, want er '
                'zijn verschillende mogelijkheden en de keuze hangt ook af van wat u zelf wilt.",\n'
                '  "justification": "The clinician explicitly identifies the problem (arthrosis) '
                "and clearly signals the need for a decision involving the patient's preferences, "
                'meeting the highest anchor."\n'
                "}"
            ),
        },
    ],
    # ---------------------------------------------------------------------
    # Item 2: Equipoise — more than one way to deal with the problem
    # ---------------------------------------------------------------------
    2: [
        {
            "transcript": (
                "Dokter: Gezien uw situatie gaan we starten met fysiotherapie. Dat is in uw geval "
                "echt het beste.\n"
                "Patiënt: Ah, oké."
            ),
            "evaluation": (
                "{\n"
                '  "score": 0,\n'
                '  "evidence": "No relevant utterance",\n'
                '  "justification": "Only one option is presented; the clinician does not '
                'indicate that more than one approach exists."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: Er zijn eigenlijk twee opties: een operatie of eerst afwachten en "
                "fysiotherapie proberen.\n"
                "Patiënt: En wat raadt u aan?\n"
                "Dokter: Tja, dat hangt van uzelf af."
            ),
            "evaluation": (
                "{\n"
                '  "score": 1,\n'
                '  "evidence": "Er zijn eigenlijk twee opties: een operatie of eerst afwachten en fysiotherapie proberen.",\n'
                '  "justification": "The options are listed but not explained; this matches the '
                '\\"listing the options\\" anchor."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: Bij uw aandoening zijn er twee gelijkwaardige behandelingen mogelijk: "
                "een borstsparende operatie met bestraling of een volledige amputatie. Beide "
                "geven een vergelijkbare overleving. Welke beter bij u past hangt echt af van "
                "wat u zelf belangrijk vindt."
            ),
            "evaluation": (
                "{\n"
                '  "score": 4,\n'
                '  "evidence": "Bij uw aandoening zijn er twee gelijkwaardige behandelingen mogelijk... '
                'Welke beter bij u past hangt echt af van wat u zelf belangrijk vindt.",\n'
                '  "justification": "The clinician explicitly states equipoise between options and '
                'ties the choice to patient preferences, meeting the highest anchor."\n'
                "}"
            ),
        },
    ],
    # ---------------------------------------------------------------------
    # Item 3: Patient's preferred approach to receiving information
    # ---------------------------------------------------------------------
    3: [
        {
            "transcript": (
                "Dokter: Ik leg het u nu mondeling uit en dan weet u alles wat u nodig heeft.\n"
                "Patiënt: Goed."
            ),
            "evaluation": (
                "{\n"
                '  "score": 0,\n'
                '  "evidence": "No relevant utterance",\n'
                '  "justification": "The clinician does not assess how the patient prefers to '
                'receive information."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: Wilt u een folder mee?\nPatiënt: Ja, graag."
            ),
            "evaluation": (
                "{\n"
                '  "score": 1,\n'
                '  "evidence": "Wilt u een folder mee?",\n'
                '  "justification": "A brief, closed question about a single information format '
                'matches the \\"short (do you want a brochure?)\\" anchor."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: We hebben verschillende manieren om de informatie aan u te geven. "
                "Ik kan het u nu uitleggen, ik kan u een folder meegeven, er is een filmpje "
                "online en er is ook een keuzehulp met grafieken. Wat past het beste bij u?\n"
                "Patiënt: Een folder en het filmpje, denk ik."
            ),
            "evaluation": (
                "{\n"
                '  "score": 4,\n'
                '  "evidence": "Ik kan het u nu uitleggen, ik kan u een folder meegeven, er is een '
                'filmpje online en er is ook een keuzehulp met grafieken. Wat past het beste bij u?",\n'
                '  "justification": "The clinician lists concrete examples of information formats '
                "and explicitly asks the patient's preference.\"\n"
                "}"
            ),
        },
    ],
    # ---------------------------------------------------------------------
    # Item 4: Listing options (including 'no action')
    # ---------------------------------------------------------------------
    4: [
        {
            "transcript": (
                "Dokter: We gaan u opereren volgende maand.\nPatiënt: Oké."
            ),
            "evaluation": (
                "{\n"
                '  "score": 0,\n'
                '  "evidence": "No relevant utterance",\n'
                '  "justification": "Only a single course of action is presented; no options are listed."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: U kunt kiezen voor een operatie of voor medicatie.\n"
                "Patiënt: Hmm."
            ),
            "evaluation": (
                "{\n"
                '  "score": 2,\n'
                '  "evidence": "U kunt kiezen voor een operatie of voor medicatie.",\n'
                '  "justification": "The clinician offers a brief choice between two options, '
                'matching the \\"little explanation of the options (you can choose ... or ...)\\" anchor."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: Er zijn drie mogelijkheden. De eerste is een open operatie waarbij we "
                "de hele aneurysma vervangen. De tweede is een endovasculaire ingreep via de "
                "lies, dat is minder belastend. De derde optie is om voorlopig niets te doen "
                "en het halfjaarlijks te controleren met een echo. Niets doen is hier echt ook "
                "een serieuze optie."
            ),
            "evaluation": (
                "{\n"
                '  "score": 3,\n'
                '  "evidence": "Er zijn drie mogelijkheden. De eerste is een open operatie... '
                "De tweede is een endovasculaire ingreep via de lies... De derde optie is om "
                'voorlopig niets te doen... Niets doen is hier echt ook een serieuze optie.",\n'
                '  "justification": "All options are listed extensively and \\"no action\\" is '
                'explicitly named as a possibility, matching the score 3 anchor."\n'
                "}"
            ),
        },
    ],
    # ---------------------------------------------------------------------
    # Item 5: Pros and cons of options
    # ---------------------------------------------------------------------
    5: [
        {
            "transcript": (
                "Dokter: U kunt kiezen tussen optie A en optie B.\n"
                "Patiënt: En wat zijn de verschillen?\n"
                "Dokter: Dat bespreken we de volgende keer wel."
            ),
            "evaluation": (
                "{\n"
                '  "score": 0,\n'
                '  "evidence": "No relevant utterance",\n'
                '  "justification": "Pros and cons are not explained at all."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: De operatie heeft als voordeel dat u snel van de klachten af bent, "
                "maar er is een risico op een wondinfectie. Bij medicatie heeft u minder snel "
                "resultaat, maar u hoeft geen ingreep te ondergaan. En als we niets doen, "
                "kan het rustig blijven of langzaam toenemen."
            ),
            "evaluation": (
                "{\n"
                '  "score": 2,\n'
                '  "evidence": "De operatie heeft als voordeel dat u snel van de klachten af bent, '
                "maar er is een risico op een wondinfectie. Bij medicatie heeft u minder snel "
                "resultaat, maar u hoeft geen ingreep te ondergaan. En als we niets doen, kan het "
                'rustig blijven of langzaam toenemen.",\n'
                '  "justification": "Pros and cons are given for all three options, matching the '
                '\\"explaining pros and cons of all options\\" anchor."\n'
                "}"
            ),
        },
    ],
    # ---------------------------------------------------------------------
    # Item 6: Patient's expectations / ideas about management
    # ---------------------------------------------------------------------
    6: [
        {
            "transcript": (
                "Dokter: We doen het zo: u krijgt eerst chemo en daarna bestraling.\n"
                "Patiënt: Ja."
            ),
            "evaluation": (
                "{\n"
                '  "score": 0,\n'
                '  "evidence": "No relevant utterance",\n'
                '  "justification": "The clinician does not explore the patient\'s expectations."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: Wat had u zelf in gedachten over hoe we dit zouden aanpakken?\n"
                "Patiënt: Ik dacht eigenlijk aan opereren.\n"
                "Dokter: Oké."
            ),
            "evaluation": (
                "{\n"
                '  "score": 2,\n'
                '  "evidence": "Wat had u zelf in gedachten over hoe we dit zouden aanpakken?",\n'
                '  "justification": "The clinician explicitly asks about expectations but does not '
                'discuss them further, matching the \\"asking the expectations (only asking)\\" anchor."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: Wat had u zelf voor beeld bij de behandeling?\n"
                "Patiënt: Ik hoopte eigenlijk dat ik met een pilletje af zou kunnen.\n"
                "Dokter: Dat begrijp ik. Wat verwacht u dan dat zo'n pil voor u zou doen, "
                "en hoe ziet u het voor zich op de langere termijn?\n"
                "Patiënt: Nou, dat ik geen pijn meer heb en gewoon kan blijven werken.\n"
                "Dokter: Helder, dan is het goed dat we dit verwachtingsbeeld even tegen de "
                "realistische resultaten aan houden."
            ),
            "evaluation": (
                "{\n"
                '  "score": 4,\n'
                '  "evidence": "Wat had u zelf voor beeld bij de behandeling?... Wat verwacht u '
                "dan dat zo'n pil voor u zou doen, en hoe ziet u het voor zich op de langere termijn?\",\n"
                '  "justification": "The clinician asks about expectations and then discusses them '
                'in depth, matching the highest anchor."\n'
                "}"
            ),
        },
    ],
    # ---------------------------------------------------------------------
    # Item 7: Patient's concerns / fears
    # ---------------------------------------------------------------------
    7: [
        {
            "transcript": (
                "Dokter: De ingreep duurt ongeveer twee uur en u blijft een nacht in het ziekenhuis.\n"
                "Patiënt: Oké."
            ),
            "evaluation": (
                "{\n"
                '  "score": 0,\n'
                '  "evidence": "No relevant utterance",\n'
                '  "justification": "The clinician does not explore the patient\'s concerns."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: Heeft u nog ergens zorgen over?\n"
                "Patiënt: Eigenlijk wel, ik ben bang voor de narcose.\n"
                "Dokter: Vertel eens, waar zit die angst precies in? Heeft u eerder een "
                "vervelende ervaring gehad?\n"
                "Patiënt: Ja, mijn moeder werd er heel ziek van.\n"
                "Dokter: Dat snap ik, laten we daar uitgebreid bij stilstaan."
            ),
            "evaluation": (
                "{\n"
                '  "score": 4,\n'
                '  "evidence": "Heeft u nog ergens zorgen over?... Vertel eens, waar zit die angst '
                'precies in? Heeft u eerder een vervelende ervaring gehad?",\n'
                '  "justification": "The clinician asks about concerns and explores them in depth, '
                'matching the highest anchor."\n'
                "}"
            ),
        },
    ],
    # ---------------------------------------------------------------------
    # Item 8: Checking patient understanding
    # ---------------------------------------------------------------------
    8: [
        {
            "transcript": (
                "Dokter: Ik heb u nu alles uitgelegd. Tot volgende week.\n"
                "Patiënt: Dank u wel."
            ),
            "evaluation": (
                "{\n"
                '  "score": 0,\n'
                '  "evidence": "No relevant utterance",\n'
                '  "justification": "The clinician does not check whether the patient has '
                'understood the information."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: Is het zo duidelijk? U mag natuurlijk altijd vragen stellen.\n"
                "Patiënt: Ja, het is duidelijk."
            ),
            "evaluation": (
                "{\n"
                '  "score": 2,\n'
                '  "evidence": "Is het zo duidelijk? U mag natuurlijk altijd vragen stellen.",\n'
                '  "justification": "The clinician asks if it is clear and invites questions, '
                'matching the \\"is it clear (you can ask questions)\\" anchor."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: Om zeker te weten dat ik het goed heb uitgelegd: zou u in uw eigen "
                "woorden kunnen herhalen wat de twee behandelopties zijn en wat de "
                "belangrijkste verschillen zijn?\n"
                "Patiënt: Eh, optie één is de operatie met een week herstel, en optie twee "
                "is medicatie waar ik langer mee bezig ben maar dan zonder ingreep."
            ),
            "evaluation": (
                "{\n"
                '  "score": 3,\n'
                '  "evidence": "zou u in uw eigen woorden kunnen herhalen wat de twee '
                'behandelopties zijn en wat de belangrijkste verschillen zijn?",\n'
                '  "justification": "The clinician checks understanding by asking the patient to '
                'repeat the information, matching the score 3 anchor."\n'
                "}"
            ),
        },
    ],
    # ---------------------------------------------------------------------
    # Item 9: Explicit opportunities to ask questions
    # ---------------------------------------------------------------------
    9: [
        {
            "transcript": (
                "Dokter: Dat was het. Tot de volgende afspraak.\nPatiënt: Dag."
            ),
            "evaluation": (
                "{\n"
                '  "score": 0,\n'
                '  "evidence": "No relevant utterance",\n'
                '  "justification": "The clinician does not offer the patient any explicit '
                'opportunity to ask questions."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: Heeft u verder nog vragen?\n"
                "Patiënt: Nee, ik denk dat ik het allemaal weet."
            ),
            "evaluation": (
                "{\n"
                '  "score": 2,\n'
                '  "evidence": "Heeft u verder nog vragen?",\n'
                '  "justification": "The clinician offers a generic opportunity to ask questions, '
                'matching the \\"possibility to ask questions (Do you have any questions)\\" anchor."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: Voordat we verder gaan: heeft u op dit moment nog vragen over de "
                "operatie zelf, over de chemotherapie, of over hoe we tot het uiteindelijke "
                "behandelplan komen? Stelt u ze gerust, ook als u denkt dat het misschien "
                "een kleine vraag is."
            ),
            "evaluation": (
                "{\n"
                '  "score": 4,\n'
                '  "evidence": "heeft u op dit moment nog vragen over de operatie zelf, over de '
                "chemotherapie, of over hoe we tot het uiteindelijke behandelplan komen? Stelt u "
                'ze gerust, ook als u denkt dat het misschien een kleine vraag is.",\n'
                '  "justification": "The clinician explicitly invites questions about specific '
                "options and treatments, and lowers the threshold for asking — matching the "
                'highest anchor."\n'
                "}"
            ),
        },
    ],
    # ---------------------------------------------------------------------
    # Item 10: Patient's preferred level of involvement in decision-making
    # ---------------------------------------------------------------------
    10: [
        {
            "transcript": (
                "Dokter: Ik heb voor u een plan gemaakt en dat gaan we zo uitvoeren.\n"
                "Patiënt: Goed dokter."
            ),
            "evaluation": (
                "{\n"
                '  "score": 0,\n'
                '  "evidence": "No relevant utterance",\n'
                '  "justification": "The clinician does not elicit the patient\'s preferred level '
                'of involvement."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: Sommige mensen willen graag zelf de keuze maken, anderen vinden het "
                "prettig als de dokter beslist en weer anderen willen het samen doen. Hoe "
                "zou u het zelf het liefst willen?\n"
                "Patiënt: Ik wil het graag samen doen, denk ik."
            ),
            "evaluation": (
                "{\n"
                '  "score": 4,\n'
                '  "evidence": "Sommige mensen willen graag zelf de keuze maken, anderen vinden '
                "het prettig als de dokter beslist en weer anderen willen het samen doen. Hoe zou "
                'u het zelf het liefst willen?",\n'
                '  "justification": "The clinician explains different involvement options in '
                'patient-friendly language and asks for the preference, matching the highest anchor."\n'
                "}"
            ),
        },
    ],
    # ---------------------------------------------------------------------
    # Item 11: Indicating need for a decision-making (or deferring) stage
    # ---------------------------------------------------------------------
    11: [
        {
            "transcript": (
                "Dokter: We hebben alles besproken. Goedendag.\n"
                "Patiënt: Tot ziens."
            ),
            "evaluation": (
                "{\n"
                '  "score": 0,\n'
                '  "evidence": "No relevant utterance",\n'
                '  "justification": "The clinician does not indicate that a decision needs to be made."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: U hoeft nu nog niet te kiezen. Neem rustig de tijd om er thuis over "
                "na te denken en ook met uw partner te bespreken. Volgende week hoor ik graag "
                "welke behandeling uw voorkeur heeft, dan stellen we samen het definitieve "
                "plan op."
            ),
            "evaluation": (
                "{\n"
                '  "score": 4,\n'
                '  "evidence": "U hoeft nu nog niet te kiezen. Neem rustig de tijd om er thuis '
                "over na te denken en ook met uw partner te bespreken. Volgende week hoor ik "
                "graag welke behandeling uw voorkeur heeft, dan stellen we samen het definitieve "
                'plan op.",\n'
                '  "justification": "The clinician explicitly indicates that a decision needs to '
                "be made, allows deferral and frames it as a shared next step, matching the "
                'highest anchor."\n'
                "}"
            ),
        },
    ],
    # ---------------------------------------------------------------------
    # Item 12: Indicating the need to review the decision (or deferment)
    # ---------------------------------------------------------------------
    12: [
        {
            "transcript": (
                "Dokter: Goed, dan is dit het plan. Veel succes.\n"
                "Patiënt: Dank u wel."
            ),
            "evaluation": (
                "{\n"
                '  "score": 0,\n'
                '  "evidence": "No relevant utterance",\n'
                '  "justification": "The clinician does not indicate any need to review the '
                'decision later."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: Ik zie u over zes weken weer terug op de poli.\n"
                "Patiënt: Oké, prima."
            ),
            "evaluation": (
                "{\n"
                '  "score": 1,\n'
                '  "evidence": "Ik zie u over zes weken weer terug op de poli.",\n'
                '  "justification": "A brief follow-up appointment is mentioned without further '
                'context, matching the \\"short (follow-up appointment)\\" anchor."\n'
                "}"
            ),
        },
        {
            "transcript": (
                "Dokter: We plannen over zes weken een vervolgafspraak om samen te evalueren "
                "hoe de behandeling bevalt. Mocht u in de tussentijd merken dat u toch liever "
                "een andere kant op wilt, dan kunt u die keuze altijd nog herzien — daar "
                "bespreken we dan opnieuw de voor- en nadelen voor."
            ),
            "evaluation": (
                "{\n"
                '  "score": 4,\n'
                '  "evidence": "We plannen over zes weken een vervolgafspraak om samen te '
                "evalueren hoe de behandeling bevalt. Mocht u in de tussentijd merken dat u toch "
                'liever een andere kant op wilt, dan kunt u die keuze altijd nog herzien.",\n'
                '  "justification": "The clinician explicitly schedules a review appointment '
                'and makes clear that the decision can be revised, matching the highest anchor."\n'
                "}"
            ),
        },
    ],
}
