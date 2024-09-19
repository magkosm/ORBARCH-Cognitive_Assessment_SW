from pyglet.window import key
import pyglet.media
from custom_functions import *
from drawing_utils import *
import csv
from messeges import *

# Reads config file and sets them as global
config_path = 'config_nback_pvt.ini'
config_values = read_config(config_path)

set_globals_from_config(config_values, globals())

# Window initiation
if fullscreen_mode:
    window = pyglet.window.Window(fullscreen=fullscreen_mode)
else:
    window = pyglet.window.Window(fullscreen=fullscreen_mode, width=window_width, height=window_height)

# Create the scale for UI elements and scale them
scale = window.height / 1000  # scalar for questionaires

scale_global_variables(scale)

win_height = window.height
win_width = window.width

# Global, Script specific vars
key_handler = key.KeyStateHandler()
audio_toggle = True
sound_played = False
# stimuli_list = ['1', '2', '3', '4', '5', '6', '8', '9', 'C', 'H', 'K', 'N', 'R', 'W', 'X', 'Y']
stimuli_list = ['C', 'H', 'K', 'N', 'R', 'W', 'X', 'Y']
stimuli_counter = 0
sq_stimuli = 1
space_key_released = True
lshift_key_released = True
rshift_key_released = True
lctrl_released = True
n_released = True
# Initialize new variables at the start of your script
rt_feedback_toggle = True
nback_sq_feedback_toggle = True
nback_av_feedback_toggle = True
early_flag = False
dot = None
highlight_left = False
highlight_right = False

responses = {}

# pvt parameters
testType = 3
fixationtime = 400
totalTime = 600
numTrials = 10
givefeedback = True
usecontinuous = True
TooFast = 200
Lapse = 500
SleepAttack = 3000
# timeIntervals = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
timeIntervals = [1000, 2000, 3000]
pvt_loop_run = 0
elapsed_time = 0
trial_pvt = 1
did_draw_cross = False
stimuli_presented = False
stimuli_present_time = None
reaction_time_recorded = False
cross_on_time = 0
dot_on_time = 0
first_run_flag = True
trial_start_time = 0
current_interval=0
feedback_draw_time=0
draw_feedback = False
pvt_end = False
subcode = "Astro"
pvt_trial_data = []
pvt_start_time = 0
early_flag_draw_time = None

#nback settings
test1 = "consonants-av"
test2 = "squares"
nMin = 1
nMax = 4
isi = 3000
dim1targs = 4
dim2targs = 4
bothtargs = 2
trialsperblock = 20
n_back_run = 0
end_of_nback = False
csv_header_written = False


# Add key handler to the window's event handlers
window.push_handlers(key_handler)

# Set to contain keys currently being held down
keys = set()

# Variable to control whether pressing the space key should have an effect
space_key_active = False

# labels
timer_label = pyglet.text.Label('',
                                font_size=int(window.height * timer_font_size_ratio),
                                x=window.width * timer_font_size_ratio,
                                y=window.height - window.height * timer_font_size_ratio,
                                anchor_x='left',
                                anchor_y='top',
                                color=timer_color)

stage_label = pyglet.text.Label('',
                                font_size=int(window.height * stage_proceed_font_size_ratio),
                                x=window.width // 2,
                                y=window.height * label_pos_ratio_height,
                                anchor_x='center',
                                anchor_y='bottom',
                                color=text_label_color,
                                width= window.width*0.7,
                                align='center',
                                multiline=True)

stage_sublabel = pyglet.text.Label('',
                                font_size=int(window.height * stage_proceed_font_size_ratio * 0.5),
                                x=window.width // 2,
                                y=(window.height * label_pos_ratio_height)-window.height*stage_proceed_font_size_ratio ,
                                anchor_x='center',
                                anchor_y='bottom',
                                color=text_label_color,
                                width= window.width*0.7,
                                align='center',
                                multiline=True)

proceed_label = pyglet.text.Label('',
                                  font_size=int(window.height * stage_proceed_font_size_ratio),
                                  x=window.width // 2,
                                  y=window.height * proceed_label_pos_ratio_height,
                                  anchor_x='center',
                                  anchor_y='bottom',
                                  color=text_label_color)

nback_instruction_label = pyglet.text.Label('',
                                            font_size=int(window.height * stage_proceed_font_size_ratio),
                                            x=window.width // 2,
                                            y=window.height * proceed_label_pos_ratio_height,
                                            anchor_x='center',
                                            anchor_y='bottom',
                                            color=text_label_color)

nback_instruction_sublabel = pyglet.text.Label('',
                                            font_size=int(window.height * stage_proceed_font_size_ratio * 0.7),
                                            x=window.width // 2,
                                            y=window.height * proceed_label_pos_ratio_height - int(window.height * stage_proceed_font_size_ratio),
                                            anchor_x='center',
                                            anchor_y='bottom',
                                            color=text_label_color)

left_button = pyglet.text.Label('[LSHIFT: Match Square]',
                                font_size=int(window.height * button_label_font_size_ratio),
                                x=window.width * button_label_font_size_ratio,
                                y=window.height * button_label_font_size_ratio,
                                anchor_x='left',
                                anchor_y='bottom',
                                color=text_buttons_color)

right_button = pyglet.text.Label('[RSHIFT: Match Letter]',
                                 font_size=int(window.height * button_label_font_size_ratio),
                                 x=window.width * (1 - button_label_font_size_ratio),
                                 y=window.height * button_label_font_size_ratio,
                                 anchor_x='right',
                                 anchor_y='bottom',
                                 color=text_buttons_color)

rt_feedback_label = pyglet.text.Label('',
                                      font_size=18,
                                      x=window.width // 2,
                                      y=window.height // 5,
                                      anchor_x='center',
                                      anchor_y='center',
                                      color=(255, 255, 255, 255))

nback_sq_feedback_label = pyglet.text.Label('',
                                            font_size=int(window.height * button_label_font_size_ratio),
                                            x=left_button.x,
                                            y=left_button.y + left_button.content_height + int(
                                                window.height * button_label_font_size_ratio) / 2,
                                            anchor_x='left',
                                            anchor_y='bottom',
                                            color=(0, 255, 0, 255))

nback_av_feedback_label = pyglet.text.Label('',
                                            font_size=int(window.height * button_label_font_size_ratio),
                                            x=right_button.x,
                                            y=right_button.y + right_button.content_height + int(
                                                window.height * button_label_font_size_ratio) / 2,
                                            anchor_x='right',
                                            anchor_y='bottom',
                                            color=(255, 0, 0, 255))

early_flag_label = pyglet.text.Label('',
                                     font_size=instructions_font_size,
                                     x=window.width // 2,
                                     y=(window.height // 2) - int(0.2 * window.height),
                                     anchor_x='center',
                                     anchor_y='center',
                                     color=text_color)  # White

body_label = pyglet.text.Label('',
                                     font_size=instructions_font_size,
                                     x=window.width // 2,
                                     y=(window.height // 2),
                                     anchor_x='center',
                                     anchor_y='center',
                                     color=text_color,
                                     width= window.width * 0.6,
                                     align='center',
                                     multiline=True,

                                        )

pvt_timer = pyglet.text.Label('',
                                 font_size=int(window.height * button_label_font_size_ratio*.5),
                                 x=window.width * (1 - button_label_font_size_ratio),
                                 y=window.height * button_label_font_size_ratio,
                                 anchor_x='right',
                                 anchor_y='bottom',
                                 color=text_buttons_color)


# Definitions for Stages of Assessment
# 1. General Introduction Slide
def introduction_screen():

    stage_label.text = intro_stage_label
    stage_label.draw()

    body_label.text = TLX_intro_lbl
    body_label.draw()

    proceed_label.text = intro_proceed_label
    proceed_label.draw()

    if key_handler[key.SPACE] and space_key_released or (key_handler[key.N] and key_handler[key.LCTRL] and  (lctrl_released or n_released)):
        global current_phase
        # Proceed to next screen when space is pressed
        current_phase = 1

# 2. Perceived Stress and Tiredness Slide
def TLX_screen():
    global current_phase
    global sliders_tlx
    # Generate sliders only at the start of this phase
    if current_phase == 1 and not sliders_tlx:
        sliders = generate_nasa_tlx_sliders(window)

    stage_label.text = TLX_label_title
    stage_label.draw()
    stage_sublabel.text = TLX_sublabel
    stage_sublabel.draw()


    # Draw sliders here
    for slider in sliders_tlx:
        slider.draw()
    proceed_label.text = intro_proceed_label
    proceed_label.draw()

    if key_handler[key.SPACE] and space_key_released or (
            key_handler[key.N] and key_handler[key.LCTRL] and (lctrl_released or n_released)):
        responses = {slider.label: slider.get_value() for slider in sliders_tlx}
        # Get the current datetime and format the filename
        filename = f"sessions/tlx-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

        # Write the dictionary to CSV
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)

            # Write the header
            writer.writerow(['Label', 'Value'])

            # Write the rows
            for label, value in responses.items():
                writer.writerow([label, value])

        current_phase = 2

# 3. Introductory Slide for PVT
def end_screen():

    stage_label.text = end_lbl_title
    stage_label.draw()
    body_label.text = end_lbl_body
    body_label.draw()
    proceed_label.text = end_lbl_prompt
    proceed_label.draw()

    outlet.push_sample(x=[100])


    if key_handler[key.SPACE] and space_key_released or (key_handler[key.N] and key_handler[key.LCTRL] and  (lctrl_released or n_released)):
        global current_phase
        current_phase = 3

## Pyglet main event functions

@window.event
def on_draw():
    # Clear screen
    global sq_stimuli, av_stimuli, space_key_released, lshift_key_released, rshift_key_released, stimuli_counter,\
           sound_played, lctrl_released, n_released, nMax

    window.clear()

    if current_phase == 0:
        introduction_screen()
    elif current_phase == 1:
        TLX_screen()
    elif current_phase == 2:
        end_screen()
    elif current_phase == 3:
        pyglet.app.exit()

    if key_handler[key.Q] and key_handler[key.LCTRL]:  # Exit on CTRL + Q
        if debug_mode:
            debug_print("CTRL + Q pressed")
        pyglet.app.exit()

    if key_handler[key.SPACE] and space_key_released:
        space_key_released = False
    elif not key_handler[key.SPACE]:
        space_key_released = True

    if key_handler[key.LCTRL] and lctrl_released:
        lctrl_released = False
    elif not key_handler[key.LCTRL]:
        lctrl_released = True

    if key_handler[key.N] and n_released:
        n_released = False
    elif not key_handler[key.N]:
        n_released = True

    if debug_mode:
        current_time = datetime.datetime.now()
        elapsed_time = current_time - start_time
        timer_label.text = str(elapsed_time)
        timer_label.draw()

@window.event
def on_key_press(symbol, modifiers):
    # Prevent default handler from being called when ESC key is pressed
    if symbol == key.ESCAPE:
        return pyglet.event.EVENT_HANDLED

def update(dt):
    pass

start_time = datetime.datetime.now()
# Establish the refresh rate for pyglet
pyglet.clock.schedule_interval(update, refresh_increment)

sliders_tlx = generate_nasa_tlx_sliders(window)
for slider in sliders_tlx:
    window.push_handlers(slider)

# Then, push key_handler
window.push_handlers(key_handler)

if True:
    # Push the key_state_handler onto the stack of event handlers
    # Define current phase
    current_phase = 0

    if debug_mode:
        debug_print("Main Loop Initiated")
    window.push_handlers(key_handler)

    introduction_screen()

    pyglet.app.run()
