from pyglet.window import key
import pyglet.media
import random
from custom_functions import *
from drawing_utils import *
import csv
import statistics
from messeges import *
from pylsl import StreamInfo, StreamOutlet

info = StreamInfo(name='cortivision_markers', type='Markers', channel_count=1,
                  channel_format='int32', source_id='pvt-orbarch')

outlet = StreamOutlet(info)
# Markers for pylsl
# 1 next stage
# 2 MATB Scenario 1
# 3 MATB Scenario 2
# 4 MATB Scenario 3
# 5 MATB Scenario 4
#
# 10 pvt stimuli
# 11 pvt response
# ((n+1)*10) n-back stimuli presented
# ((n+1)*10)+1 n-back audiovisual resp
# ((n+1)*10)+2 n-back visuospatial resp

# Reads config file and sets them as global
config_path = 'config_nback_pvt.ini'
config_values = read_config(config_path)
set_globals_from_config(config_values, globals())
print(config_values)

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
stimuli_outlet_pushed = False
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
pvt_trial_data = []
pvt_start_time = 0
early_flag_draw_time = None

#nback parameters
n_back_run = 0
end_of_nback = False
csv_header_written = False


# Add key handler to the window's event handlers
window.push_handlers(key_handler)

# Set to contain keys currently being held down
keys = set()

# Variable to control whether pressing the space key should have an effect
space_key_active = False

nback_image = pyglet.image.load('includes/img/nback.png')

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
                                y=(window.height * label_pos_ratio_height)-window.height*stage_proceed_font_size_ratio,
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

left_button = pyglet.text.Label('[L Shift: Match Square]',
                                font_size=int(window.height * button_label_font_size_ratio),
                                x=window.width * button_label_font_size_ratio,
                                y=window.height * button_label_font_size_ratio,
                                anchor_x='left',
                                anchor_y='bottom',
                                color=text_buttons_color)

right_button = pyglet.text.Label('[R Shift: Match Letter]',
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
                                            y=(left_button.y + left_button.content_height + int(
                                                window.height * button_label_font_size_ratio) / 2) ,
                                            anchor_x='left',
                                            anchor_y='bottom',
                                            color=(0, 255, 0, 255))

nback_av_feedback_label = pyglet.text.Label('',
                                            font_size=int(window.height * button_label_font_size_ratio),
                                            x=right_button.x,
                                            y=(right_button.y + right_button.content_height + int(
                                                window.height * button_label_font_size_ratio) / 2) ,
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

body_label_left = pyglet.text.Label('',
                                     font_size=instructions_font_size,
                                     x=window.width * 0.02,
                                     y=(window.height // 2),
                                     anchor_x='left',
                                     anchor_y='center',
                                     color=text_color,
                                     width= window.width * 0.6,
                                     align='left',
                                     multiline=True,

                                        )

pvt_timer = pyglet.text.Label('',
                                 font_size=int(window.height * button_label_font_size_ratio*.5),
                                 x=window.width * (1 - button_label_font_size_ratio),
                                 y=window.height * button_label_font_size_ratio,
                                 anchor_x='right',
                                 anchor_y='bottom',
                                 color=text_buttons_color)

def time_diff_in_ms(t1: datetime.time, t2: datetime.time) -> float:
    return ((t2.hour - t1.hour) * 3600 +(t2.minute - t1.minute) * 60 +t2.second - t1.second) * 1000 + (t2.microsecond - t1.microsecond) / 1000

def generate_pvt_report():
    # Get the current date and time
    current_time = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")

    # Initialize data structures for report
    intervals = {}
    total_counts = {
        "Too Fast": 0,
        "Correct": 0,
        "Lapse": 0,
        "Sleep Attack": 0
    }

    # Process pvt_trial_data to accumulate stats
    for trial in pvt_trial_data:
        response_type = trial['type']
        isi_bin = trial['ISIbin']

        if isi_bin not in intervals:
            intervals[isi_bin] = {"count": 0, "reaction_times": []}
        intervals[isi_bin]["count"] += 1
        intervals[isi_bin]["reaction_times"].append(trial['rt'])

        # Increment the response type count
        if response_type == 1:
            total_counts["Too Fast"] += 1
        elif response_type == 2:
            total_counts["Correct"] += 1
        elif response_type == 3:
            total_counts["Lapse"] += 1
        elif response_type == 4:
            total_counts["Sleep Attack"] += 1

    # Start writing to the report
    report = []
    report.append(current_time)
    report.append(f"Participant Code: {subcode}")
    report.append("--------------------------------------------------------")
    report.append("Delay\tCount\tMedian RT\tMean RT\t\tSD RT")
    report.append("--------------------------------------------------------")

    for isi_bin, data in intervals.items():
        count = data["count"]
        median_rt = statistics.median(data["reaction_times"])
        mean_rt = statistics.mean(data["reaction_times"])

        # Handle SD calculation for cases with less than 2 samples
        if len(data["reaction_times"]) > 1:
            sd_rt = statistics.stdev(data["reaction_times"])
        elif len(data["reaction_times"]) == 1:
            sd_rt = 0  # Standard deviation of a single value is 0
        else:
            sd_rt = 'NA'  # Not available/applicable for zero values

        report.append(f"{isi_bin}\t{count}\t{median_rt:.2f}\t\t{mean_rt:.2f}\t\t{sd_rt}")

    report.append("--------------------------------------------------------")
    for k, v in total_counts.items():
        report.append(f"{k}:\t\t{v}")
    report.append("--------------------------------------------------------")

    # Save the report to a TXT file
    with open(f"sessions/pvt-report-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt", 'w') as txtfile:
        for line in report:
            txtfile.write(line + "\n")

## Definitions and functions for n-back sequence generator
# 1. Initialize settings
def init_settings():
    settings = {
        "test1": test1,
        "test2": test2,
        "nMin": nmin,
        "nMax": nmax,
        "isi": isi,
        "dim1targs": dim1targs,
        "dim2targs": dim2targs,
        "bothtargs": bothtargs,
        "trialsperblock": trialsperblock
    }
    return settings

# 2. Generate the N-Back design
def generate_design(n, dim1targs, dim2targs, bothtargs, trials):
    # Create base designs without matches
    base_design = [[0, 0] for _ in range(n)]

    # Create the rest of the design without the first n items
    rest_of_design = [
                         [1, 0] for _ in range(dim1targs)
                     ] + [
                         [0, 1] for _ in range(dim2targs)
                     ] + [
                         [1, 1] for _ in range(bothtargs)
                     ] + [
                         [0, 0] for _ in range(trials - dim1targs - dim2targs - bothtargs - n)
                         # subtract n for the initial base_design
                     ]

    # Shuffle the rest of the design
    random.shuffle(rest_of_design)

    # Combine the base design (first n items) with the shuffled rest
    design = base_design + rest_of_design

    return design

# 3. Generate the stimuli sequence
def generate_stimuli_sequence(design, n):
    sampset = list(range(1, 9))
    dim1stim, dim2stim = random.sample(sampset, n), random.sample(sampset, n)
    for i in range(n, len(design)):
        des = design[i]
        if des[0] == 0:
            dim1val = random.choice([x for x in sampset if x != dim1stim[i-n]])
        else:
            dim1val = dim1stim[i-n]
        if des[1] == 0:
            dim2val = random.choice([x for x in sampset if x != dim2stim[i-n]])
        else:
            dim2val = dim2stim[i-n]
        dim1stim.append(dim1val)
        dim2stim.append(dim2val)
    return dim1stim, dim2stim

# Class for capturing trial information
class TrialLog_nback:
    def __init__(self):
        self.subcode = subcode  # Placeholder; you'd set this dynamically per user
        self.block = "t"  # Assuming p for practice, adjust as needed
        self.trial = 0  # Should be incremented with every trial
        self.dim1 = "AV-CONSONANTS"  # Placeholder
        self.dim2 = "SQUARES"  # Placeholder
        self.nDim = 2  # Placeholder
        self.n = None
        self.isi = None  # Placeholder
        self.d1 = None
        self.d2 = None
        self.d3 = None
        self.d4 = None
        self.dotext = 1
        self.doaudio = 1
        self.dospatial = 1
        self.timestart = 0
        self.resp1 = None
        self.corr1 = None
        self.time2 = None
        self.rta = None
        self.resp2 = None
        self.corr2 = None
        self.time3 = None
        self.rtb = None

    def as_list(self):
        return [self.subcode, self.block, self.trial, self.dim1, self.dim2, self.nDim, self.n,
                self.isi, self.d1, self.d2, self.d3, self.d4, self.dotext, self.doaudio,
                self.dospatial, self.timestart, self.resp1, self.corr1, self.time2, self.rta,
                self.resp2, self.corr2, self.time3, self.rtb]

def write_to_log_nback(log: TrialLog_nback, file_name="user_responses.csv"):
    with open(file_name, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(log.as_list())

# Definitions for Stages of Assessment
# 1. General Introduction Slide
def introduction_screen():

    stage_label.text = intro_stage_label
    stage_label.draw()

    body_label.text = intro_body_label
    body_label.draw()

    proceed_label.text = intro_proceed_label
    proceed_label.draw()



    if key_handler[key.SPACE] and space_key_released or (key_handler[key.N] and key_handler[key.LCTRL] and  (lctrl_released or n_released)):
        global current_phase
        # Proceed to next screen when space is pressed
        outlet.push_sample(x=[1])
        if debug_mode: debug_print("Pushed Marker 1")
        current_phase = 1

# 2. Perceived Stress and Tiredness Slide
def perceived_stress_and_tiredness_screen():
    global current_phase
    global sliders_pss
    # Generate sliders only at the start of this phase
    if current_phase == 1 and not sliders_pss:
        sliders = generate_pss_sliders(window)

    stage_label.text = pss_stage_label
    stage_label.draw()
    stage_sublabel.text = pss_sublabel
    stage_sublabel.draw()


    # Draw sliders here
    for slider in sliders_pss:
        slider.draw()
    proceed_label.text = intro_proceed_label
    proceed_label.draw()

    if key_handler[key.SPACE] and space_key_released or (
            key_handler[key.N] and key_handler[key.LCTRL] and (lctrl_released or n_released)):
        outlet.push_sample(x=[1])

        if debug_mode: debug_print("Pushed Marker 1")
        responses = {slider.label: slider.get_value() for slider in sliders_pss}
        # Get the current datetime and format the filename
        filename = f"sessions/pss-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

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
def pvt_intro_screen():

    stage_label.text = pvt_stage_label
    stage_label.draw()
    body_label.text = pvt_body_label
    body_label.draw()
    proceed_label.text = intro_proceed_label
    proceed_label.draw()

    if key_handler[key.SPACE] and space_key_released or (key_handler[key.N] and key_handler[key.LCTRL] and  (lctrl_released or n_released)):
        global current_phase
        outlet.push_sample(x=[1])

        if debug_mode: debug_print("Pushed Marker 1")
        current_phase = 3

# 4. Start Slide
def start_screen():
    pyglet.text.Label('[Press SPACE to start Assessment]', font_size=36, x=window.width//2, y=window.height//2, anchor_x='center', color=(255, 255, 255, 255)).draw()

    if key_handler[key.SPACE] and space_key_released or (key_handler[key.N] and key_handler[key.LCTRL] and  (lctrl_released or n_released)):
        global current_phase
        outlet.push_sample(x=[1])

        if debug_mode: debug_print("Pushed Marker 1")
        current_phase = 4

# Stage 5: PVT Assessment
def pvt_assessment():

    global current_phase, space_key_released, lctrl_released, n_released, totalTime, pvt_loop_run, elapsed_time, \
        trial_pvt, did_draw_cross, stimuli_presented, stimuli_present_time, reaction_time_recorded, cross_on_time, \
        dot_on_time, first_run_flag, trial_start_time, current_interval, draw_feedback, feedback_draw_time, pvt_end, \
        subcode, pvt_start_time, early_flag_draw_time, stimuli_outlet_pushed




    nback_instruction_label.text = pvt_instr_label
    nback_instruction_sublabel.text = pvt_react_label
    nback_instruction_label.draw()
    nback_instruction_sublabel.draw()

    if pvt_loop_run == 0:
        pvt_start_time = datetime.datetime.now().time()
        # Time since trial start
        trial_pvt = 1
        first_run_flag = True
        # States for the flow of the assessment
        did_draw_cross = False
        cross_on_time = 0
        stimuli_presented = False
        # Also reset the new flag so that the outlet can be pushed again for the next stimuli
        stimuli_outlet_pushed = False
        stimuli_present_time = 0
        pvt_end = False

        if debug_mode: debug_print(f"PVT Loop intitiated with start_time: {pvt_start_time}.")
    pvt_loop_run += 1
    current_time = datetime.datetime.now().time()

    if first_run_flag:
        first_run_flag = False
        current_interval = random.choice(timeintervals)
        current_datetime = datetime.datetime.now()
        trial_start_time = current_datetime.time()
        stimuli_present_datetime = current_datetime + datetime.timedelta(milliseconds=current_interval)
        stimuli_present_time = stimuli_present_datetime.time()


    if not did_draw_cross or (time_diff_in_ms(cross_on_time, current_time) <= fixationtime):
        if not did_draw_cross:
            cross_on_time = datetime.datetime.now().time()
            if debug_mode: debug_print('Fixation Cross Drawn')
        draw_cross(win_width, win_height, cross_arm_length_ratio, cross_line_width_ratio, cross_color)
        did_draw_cross = True

    if time_diff_in_ms(trial_start_time, current_time) >= current_interval:
        draw_dot(win_width, win_height, dot, dot_radius_ratio, dot_color)

        stimuli_presented = True

    if debug_mode and (time_diff_in_ms(trial_start_time, current_time) <= current_interval):
        countdown = (math.floor(current_interval - (time_diff_in_ms(trial_start_time, current_time))))
        pvt_timer.text = f"Next Stimuli in {countdown} ms."
        pvt_timer.draw()

    if debug_mode and stimuli_presented:
        time_passed = math.floor(time_diff_in_ms(stimuli_present_time, current_time))
        pvt_timer.text = f"Time passed since stimuli was presented: {time_passed} ms"
        pvt_timer.draw()

    if stimuli_presented:
        current_time = datetime.datetime.now().time()

        if key_handler[key.SPACE]:  # if SPACE key is pressed
            # calculate reaction time
            reaction_time = math.floor(time_diff_in_ms(stimuli_present_time, current_time))
            outlet.push_sample(x=[11])
            if debug_mode: debug_print("Pushed Marker 11")

            if debug_mode: debug_print(f'Reaction Logged as {reaction_time} ms.')

            if reaction_time < toofast:
                response_type = 1
            elif toofast <= reaction_time < lapse:
                response_type = 2
            elif lapse <= reaction_time < sleepattack:
                response_type = 3
            else:
                response_type = 4

            abstime = time_diff_in_ms(pvt_start_time, current_time)

            # Append data for the trial
            pvt_trial_data.append({
                'sub': subcode,
                'block': 1,  # default value; modify as necessary
                'trial': trial_pvt,
                'ISI': time_diff_in_ms(stimuli_present_time, current_time),
                'ISIbin': current_interval,
                'abstime': abstime,
                'rt': reaction_time,
                'type': response_type
            })

            if provide_feedback:
                rt_feedback_label.text = f"[{reaction_time} ms]"
                feedback_draw_time = datetime.datetime.now().time()
                draw_feedback = True



            # Reset Flags
            did_draw_cross = False
            stimuli_presented = False
            reaction_time_recorded = False
            stimuli_outlet_pushed = False

            # Set up next trials by selecting new interval
            current_interval = random.choice(timeintervals)
            current_datetime = datetime.datetime.now()
            trial_start_time = current_datetime.time()
            stimuli_present_datetime = current_datetime + datetime.timedelta(milliseconds=current_interval)
            stimuli_present_time = stimuli_present_datetime.time()
            trial_pvt += 1

    if stimuli_presented and not stimuli_outlet_pushed:
        # Your new line to run only once when stimuli is presented
        outlet.push_sample(x=[10])
        if debug_mode: debug_print("Pushed Marker 10")
        if debug_mode: debug_print('Circle Stimuli Drawn')
        # Set the flag to True so that the line doesn't run again until reset
        stimuli_outlet_pushed = True

    elif key_handler[key.SPACE] and space_key_released:
        if debug_mode: debug_print('Space pressed before stimuli, 500ms added to timer to next stimuli')
        early_flag_label.text = pvt_early_react_lbl
        early_flag_label.draw()
        early_flag_draw_time = datetime.datetime.now().time()  # Record the time
        current_interval += 500

    if early_flag_draw_time and (time_diff_in_ms(early_flag_draw_time, current_time) <= fixationtime):
        early_flag_label.draw()

    if draw_feedback and (time_diff_in_ms(feedback_draw_time, current_time) < fixationtime):
        rt_feedback_label.draw()

    if testtype == 1 and (time_diff_in_ms(pvt_start_time, current_time) >= totaltime):
        pvt_end = True
    elif testtype == 3 and trial_pvt > numtrials:
        print("end type3")
        pvt_end = True

    if (key_handler[key.N] and key_handler[key.LCTRL] and  (lctrl_released or n_released)):
        pvt_end = True

    if pvt_end:
        # Save data to CSV
        if debug_mode: debug_print('Printing to CSV')
        file_name = f"sessions/pvt-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        with open(file_name, 'w', newline='') as csvfile:
            fieldnames = ['sub', 'block', 'trial', 'ISI', 'ISIbin', 'abstime', 'rt', 'type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in pvt_trial_data:
                writer.writerow(row)

        global current_phase
        outlet.push_sample(x=[1])

        if debug_mode: debug_print("Pushed Marker 1")
        current_phase = 5

# Stage 6: PVT End of Assessment Screen
def pvt_end_screen():
    global current_phase
    stage_label.text = pvt_stage_label
    stage_label.draw()
    body_label.text = pvt_end_body
    body_label.draw()
    proceed_label.text = pvt_report_prompt
    proceed_label.draw()

    if key_handler[key.Y]:  # if Y key is pressed
        if debug_mode: debug_print('Generating Report')
        generate_pvt_report()

        current_phase = 6

    if key_handler[key.SPACE] and space_key_released or (
            key_handler[key.N] and key_handler[key.LCTRL] and (lctrl_released or n_released)):
        outlet.push_sample(x=[1])

        if debug_mode: debug_print("Pushed Marker 1")
        current_phase = 6

# Stage 7: Introductory Slide for n-Back assessment
def nback_introduction(nMin, nMax):
    stage_label.text = nback_title_lbl
    stage_label.draw()
    body_label_left.text = nback_instr_label(nmin,nmax)

    body_label_left.draw()
    proceed_label.text = intro_proceed_label
    proceed_label.draw()

    # Calculate the scaling factor and position for the image
    # Adjust these values as needed to get the desired effect
    image_height = window.height * 0.4
    scale = image_height / nback_image.height
    image_width = nback_image.width * scale
    image_x = window.width- image_width*1.1  # Align to the right
    image_y = (window.height - image_height) / 2  # Center vertically

    nback_image.blit(x=image_x, y=image_y, width=image_width, height=image_height)

    if key_handler[key.SPACE] and space_key_released or (
            key_handler[key.N] and key_handler[key.LCTRL] and (lctrl_released or n_released)):
        global current_phase
        outlet.push_sample(x=[1])

        if debug_mode: debug_print("Pushed Marker 1")
        current_phase = 7

# Stage 8: modular slide (n-step) Start of stage
def nback_start(n):
    global file_name_nback
    global csv_header_written

    stage_label.text = f'{n}-Back Working Memory Task'
    stage_label.draw()
    body_label.text = nback_stage_instr_lbl(n)
    body_label.draw()
    proceed_label.text = intro_proceed_label
    proceed_label.draw()

    if not csv_header_written:
        csv_header_written = True
        # Ensure the CSV header is written at the beginning of the program or session
        file_name_nback = f"sessions/nback-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        with open(file_name_nback, "w", newline='') as file:
            writer = csv.writer(file)
            header = ["subcode", "block", "trial", "dim1", "dim2", "nDim", "n", "isi",
                      "d1", "d2", "d3", "d4", "dotext", "doaudio", "dospatial",
                      "timestart", "resp1", "corr1", "time2", "rta", "resp2", "corr2", "time3", "rtb"]
            writer.writerow(header)

    if key_handler[key.SPACE] and space_key_released or (key_handler[key.N] and key_handler[key.LCTRL] and  (lctrl_released or n_released)):
        global current_phase
        outlet.push_sample(x=[1])

        if debug_mode: debug_print("Pushed Marker 1")
        current_phase += 1
# Stage 9: modular slide (n-step) Assessment
def nback(n):
    global space_key_released, lshift_key_released, rshift_key_released, sound_played, lctrl_released,n_back_run,\
        end_of_nback, sq_stimuli, av_stimuli, current_stimuli, nback_start_time, settings, trial_log, design, \
        file_name_nback, av_trig_flag, av_trig_timer, sq_trig_flag, sq_trig_timer

    squares = create_grid(win_height, win_width, grid_size_ratio)
    left_button.draw()
    right_button.draw()
    draw_grid(squares)
    draw_nb_instruction(nback_instruction_label, debug_mode)
    stage_label.text = f"Match [{n}]-back."
    stage_label.draw()

    if n_back_run == 0:
        nback_start_time = datetime.datetime.now().time()
        settings= init_settings()
        design = generate_design(n, settings["dim1targs"], settings["dim2targs"], settings["bothtargs"], settings["trialsperblock"])
        dim1stim, dim2stim = generate_stimuli_sequence(design, n)
        current_stimuli = 0
        sq_stimuli = dim2stim
        av_stimuli = [stimuli_list[i-1] for i in dim1stim]
        end_of_nback = False
        sq_trig_flag = False
        av_trig_flag = False
        sq_trig_time = 0
        av_trig_timer = 0


        if debug_mode:
            debug_print(f"AV_Stimuli list: {av_stimuli}")
            debug_print(f"Sq_Stimuli list: {sq_stimuli}")
    n_back_run += 1

    if current_stimuli < len(av_stimuli):
        draw_filled_square(sq_stimuli[current_stimuli], squares, filled_square_color, filled_square_size_ratio)
        draw_visual(av_stimuli[current_stimuli], squares, win_width, win_height, visual_size_ratio, text_color)
        if audio_toggle and not sound_played:
            play_sound(av_stimuli[current_stimuli], audio_files)
            sound_played = True
            outlet.push_sample(x=[(n+1)*10])

            if debug_mode: debug_print(f"Pushed Marker {[(n+1)*10]}")



    else:
        end_of_nback = True
    curr_time = datetime.datetime.now().time()
    #Move to next stimuli after ISI
    if (time_diff_in_ms(nback_start_time, curr_time)) >= (settings["isi"] * (current_stimuli + 1)):
        print(time_diff_in_ms(nback_start_time, curr_time) * (current_stimuli + 1))
        print(settings["isi"] * (current_stimuli + 1))

        trial_log = TrialLog_nback()

        trial_log.block = f"t{n}"
        trial_log.trial = current_stimuli
        trial_log.n = n
        trial_log.isi = settings["isi"]
        trial_log.d1 = design[current_stimuli][0]
        trial_log.d2 = design[current_stimuli][1]
        trial_log.d3 = av_stimuli[current_stimuli]
        trial_log.d4 = sq_stimuli[current_stimuli]
        trial_log.timestart = time_diff_in_ms(nback_start_time, curr_time) - 3000
        if av_trig_flag == True:
            trial_log.resp1 = 1
            trial_log.time2 = time_diff_in_ms(nback_start_time, av_trig_timer)
            trial_log.rta = trial_log.time2 - trial_log.timestart
        else:
            trial_log.resp1 = 0
        if trial_log.resp1 == trial_log.d1:
            trial_log.corr1 = 1
        else:
            trial_log.corr1 = 0

        if sq_trig_flag == True:
            trial_log.resp2 = 1
            trial_log.time3 = time_diff_in_ms(nback_start_time, sq_trig_timer)
            trial_log.rtb = trial_log.time3 - trial_log.timestart
        else:
            trial_log.resp2 = 0
        if trial_log.resp2 == trial_log.d2:
            trial_log.corr2 = 1
        else:
            trial_log.corr2 = 0


        write_to_log_nback(trial_log, file_name_nback)
        sq_trig_flag = False
        av_trig_flag = False
        sq_trig_time = 0
        av_trig_timer = 0
        current_stimuli += 1
        sound_played = False

    if provide_feedback:
        if av_trig_flag:
            if design[current_stimuli][0] == 1:
                draw_nback_av_feedback(True,  nback_av_feedback_label,  provide_feedback)
            else:
                draw_nback_av_feedback(False,  nback_av_feedback_label,  provide_feedback)
        if sq_trig_flag:
            if design[current_stimuli][1] == 1:
                draw_nback_sq_feedback(True, nback_sq_feedback_label, provide_feedback)
            else:
                draw_nback_sq_feedback(False, nback_sq_feedback_label, provide_feedback)



    if key_handler[key.LSHIFT]:
        if lshift_key_released:
            if debug_mode: debug_print("LSHIFT pressed")
            outlet.push_sample(x=[((n + 1) * 10) + 2])
            if debug_mode: debug_print(f"Pushed Marker {((n + 1) * 10) + 2}")
        lshift_key_released = False
        draw_rectangle(left_button.x, left_button.y, left_button.content_width,
                       left_button.content_height, rectangle_highlight_line_thickness,
                       rectangle_highlight_offset, highlight_button_color)

        if not sq_trig_flag:
            sq_trig_flag = True
            sq_trig_timer = curr_time
    elif not key_handler[key.LSHIFT]:
        lshift_key_released = True

    if key_handler[key.RSHIFT]:
        if rshift_key_released:
            if debug_mode: debug_print("RSHIFT pressed")
            outlet.push_sample(x=[((n + 1) * 10) + 1])
            if debug_mode: debug_print(f"Pushed Marker {((n + 1) * 10) + 1}")
        rshift_key_released = False
        draw_rectangle(right_button.x - right_button.content_width, right_button.y,
                       right_button.content_width, right_button.content_height,
                       rectangle_highlight_line_thickness, rectangle_highlight_offset,
                       highlight_button_color)

        if not av_trig_flag:
            av_trig_flag = True
            av_trig_timer = curr_time
    elif not key_handler[key.RSHIFT]:
        rshift_key_released = True


    if (key_handler[key.N] and key_handler[key.LCTRL] and  (lctrl_released or n_released)):
        end_of_nback = True
    if end_of_nback:
        n_back_run = 0
        global current_phase
        current_phase += 1
# Stage 10: modular slide (n-step) end of phase
def nback_end(n):
    global current_phase
    stage_label.text = f'{n}-Back Working Memory Task'
    stage_label.draw()
    body_label.text = nback_end_stage_lbl(n)
    body_label.draw()
    proceed_label.text = intro_proceed_label
    proceed_label.draw()

    if key_handler[key.SPACE] and space_key_released or (
            key_handler[key.N] and key_handler[key.LCTRL] and (lctrl_released or n_released)):
        outlet.push_sample(x=[1])
        if debug_mode: debug_print("Pushed Marker 1")
        current_phase += 1
# Stage 11: End of n-back Assessment
def nback_total_end():
    global current_phase
    stage_label.text = nback_title_lbl
    stage_label.draw()
    body_label.text = nback_end_lbl
    body_label.draw()
    proceed_label.text = intro_proceed_label
    proceed_label.draw()



    if key_handler[key.SPACE] and space_key_released or (
            key_handler[key.N] and key_handler[key.LCTRL] and (lctrl_released or n_released)):
        outlet.push_sample(x=[1])
        if debug_mode: debug_print("Pushed Marker 1")
        current_phase += 1
# Stage 13: End of Assessment
def Proceed_to_OpenMATB():
    global current_phase
    stage_label.text = MATB_label_title
    stage_label.draw()
    body_label.text = MATB_label_body
    body_label.draw()
    proceed_label.text = intro_proceed_label
    proceed_label.draw()

    if key_handler[key.SPACE] and space_key_released or (
            key_handler[key.N] and key_handler[key.LCTRL] and (lctrl_released or n_released)):
        outlet.push_sample(x=[1])

        if debug_mode: debug_print("Pushed Marker 1")

        current_phase += 1


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
        perceived_stress_and_tiredness_screen()
    elif current_phase == 2:
        pvt_intro_screen()
    elif current_phase == 3:
        start_screen()
    elif current_phase == 4:
        pvt_assessment()
    elif current_phase == 5:
        pvt_end_screen()
    elif current_phase == 6:
        nback_introduction(nmin, nmax)
    else:
        relative_phase = (current_phase - 7) % 3
        n_value = (current_phase - 7) // 3 + nmin

        if nmin <= n_value <= nmax:
            if relative_phase == 0:
                nback_start(n_value)
            elif relative_phase == 1:
                nback(n_value)
            elif relative_phase == 2:
                nback_end(n_value)
        else:
            # Considering you've exhausted the phases for nMin to nMax
            adjusted_phase = current_phase - 3 * (nmax  - nmin + 1) - 6

            if adjusted_phase == 1:
                nback_total_end()
            elif adjusted_phase == 2:
                Proceed_to_OpenMATB()
            else:
                pyglet.app.exit()




    # draw_nback_sq_feedback(correct, elapsed_time, nback_sq_feedback_label, debug_mode, provide_feedback)
    # draw_nback_av_feedback(correct, elapsed_time, nback_av_feedback_label, debug_mode, provide_feedback)
    # draw_early_flag(early_flag_label, provide_feedback, debug_mode)
    #
    # if audio_toggle and not sound_played:
    #     play_sound(stimuli_list[stimuli_counter], audio_files)
    #     sound_played = True
    #     if correct:
    #         correct = False
    #     else:
    #         correct = True

    if key_handler[key.Q] and key_handler[key.LCTRL]:  # Exit on CTRL + Q
        # Stop the LSL stream
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


# initialization of important variables




start_time = datetime.datetime.now()
# Establish the refresh rate for pyglet
pyglet.clock.schedule_interval(update, refresh_increment)

sliders_pss = generate_pss_sliders(window)
for slider in sliders_pss:
    window.push_handlers(slider)
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

    pyglet.app.run()
