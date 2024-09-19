# messages.py


intro_stage_label = 'Orbital Architecture \n Cognitive Assessment'

intro_body_label = "Welcome to the Cognitive Assessment.\n " \
                   "Before starting, we would request you to indicate your perceived stress and tiredness in the next screen."

intro_proceed_label = '[Press SPACE when you are ready to proceed]'

pss_stage_label = 'Perceived Stress and Tiredness'

pss_sublabel = '[Please use the sliders to indicate your responses to the following prompts.]'

pvt_stage_label = 'Psychomotor Vigilance Task'

pvt_body_label = "In this test, you will react to a visual stimulus (red circle) presented at the center of the " \
                 "screen. \n\nDo not press anything when you see the white cross. \n\nPress the SPACE key as soon " \
                 "as you see the red circle."

pvt_instr_label = "[Respond to the red circle, not the cross]"

pvt_react_label = "Respond by pressing the space key"

pvt_early_react_lbl = "[Wait for the red circle]"

pvt_end_body = "[This is the end of the Psychomotor Vigilance Task]"

pvt_report_prompt = '[Press SPACE to Proceed.]'

nback_title_lbl = 'n-Back Working Memory Task'

nback_end_lbl = "[This is the end of the n-Back Task]"

MATB_label_title = 'Multi-Attribute Task Battery'
MATB_label_body = "You have completed the first two tasks. Proceed to the Multi-Attribute Task Battery assessment next. "

TLX_intro_lbl = "You successfully completed all cognitive assessments.\n\nA short questionnaire about your " \
                "perceived performance remains."

TLX_label_title = 'Task Load Index Questionnaire'

TLX_sublabel = '[Please use the sliders to indicate your responses to the following prompts.]'

end_lbl_title = 'End of Assessment'

end_lbl_body = "All assessments are now completed."

end_lbl_prompt = '[Press SPACE to exit]'


def nback_instr_label(nmin, nmax):
    return f"In the following tests, you will be presented with a series of stimuli in sequence.\n\nThese " \
           f"stimuli will be delivered through two dimensions that will be presented simultaneously.\n\nThe " \
           f"first dimension of the stimuli is the audiovisual one, where you will be presented with a " \
           f"letter both visually and phonetically, always located at the center of a 3 by 3 grid.\n\nThe second dimension is a " \
           f"visuospatial stimulus, where you will be presented with a white square in one of 8 possible locations " \
           f"(around the letter).\n\n The assessment will begin at stage {nmin}-back and will end at stage {nmax}-back." \
           f"\n\nIn each of the stages, your goal is to identify matches between the current and the previous 1,2,3 or 4 stimuli " \
           f"(1-back until 4-back match)" \
           f"\n\n To indicate a match with a letter, use the [Right Shift] key\n" \
           f"To indicate a match in the white square, use the [Left Shift] Key."

def nback_stage_instr_lbl(n):
    return f"In this stage, you will need to indicate if there is a match {n} step(s) back in the sequence you " \
           f"will be presented with.\n\n To indicate a" \
           f" match wih a letter, use the [Right Shift] key\n\nTo indicate a match with the" \
           f" white square, use the [Left Shift] Key."


def nback_end_stage_lbl(n):
    return f"[This concludes the {n}-back stage of the n-Back Assessment]"
