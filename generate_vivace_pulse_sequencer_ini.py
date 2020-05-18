# Authored by Johan Blomberg and Gustav Grännsjö, 2020

import ini_generator as generator

gen = generator.Generator()
FILENAME = 'Vivace_Pulse_Sequencer.ini'
MAX_TEMPLATES = 15
CUSTOM_TEMPLATES = 4
MAX_PULSE_DEFS = 16
TEMPLATES = ['Square', 'Long drive', 'Sin2', 'SinP', 'Sinc', 'Triangle', 'Gaussian', 'Cool']
TEMPLATES.extend([f'Custom {i}' for i in range(1, CUSTOM_TEMPLATES + 1)])
NAME = 'Vivace Pulse Sequencer'
VERSION = '1.2'
DRIVER_PATH = 'Vivace_Pulse_Sequencer'
INTERFACE = 'TCPIP'


def section_general():
    section = 'General settings'
    group = 'Settings'

    # Average
    gen.create_quant('Average', 'Number of averages', 'DOUBLE', group, section)
    gen.limits(low=1)
    gen.default(1)
    gen.set_cmd('int')
    gen.show_in_measurement(True)

    # Trigger period
    gen.create_quant('Trigger period', 'Trigger period', 'DOUBLE', group, section)
    gen.limits(low=0)
    gen.default(200E-6)
    gen.show_in_measurement(True)

    # Iterations
    gen.create_quant('Iterations', 'Iterations', 'DOUBLE', group, section)
    gen.limits(low=1)
    gen.default(1)
    gen.set_cmd('int')
    gen.show_in_measurement(True)

    # -- Output stuff --
    group = 'Time trace output selection'
    # The sampling window to look at
    gen.create_quant('Index of displayed time trace - iteration', 'Iteration', 'DOUBLE', group, section)
    gen.default(1)
    gen.limits(low=1)
    gen.tooltip('Which measurement iteration to output a trace for.')
    gen.set_cmd('int', 'not_affecting_board')
    gen.show_in_measurement(True)

    gen.create_quant('Index of displayed time trace - sample pulse', 'Sampling pulse', 'DOUBLE', group, section)
    gen.default(1)
    gen.limits(low=1)
    gen.tooltip('Which sampling pulse in the given iteration to output a time trace for.')
    gen.set_cmd('int', 'not_affecting_board')
    gen.show_in_measurement(True)


def section_templates():
    section = 'Envelopes'
    group = 'General'

    # Choose how many
    gen.create_quant('Envelope template count', 'No. of envelope templates', 'COMBO', group, section)
    gen.combo_options(*[str(i) for i in range(1, MAX_TEMPLATES+1)])

    # Template definitions
    for i in range(1, MAX_TEMPLATES+1):
        group = f'Envelope template {i}'

        # Template
        gen.create_quant(f'Envelope template {i}: shape', 'Envelope shape', 'COMBO', group, section)
        gen.combo_options(*TEMPLATES)
        gen.visibility(f'Envelope template count', *[str(j) for j in range(i, MAX_TEMPLATES+1)])

        # sinP P
        gen.create_quant(f'Envelope template {i}: sinP Value', 'P', 'DOUBLE', group, section)
        gen.limits(low=0)
        gen.visibility(f'Envelope template {i}: shape', 'SinP')

        # sinc limits
        gen.create_quant(f'Envelope template {i}: sinc cutoff', 'Cutoff', 'DOUBLE', group, section)
        gen.unit('PI')
        gen.default(4)
        gen.limits(low=1e-9)
        gen.visibility(f'Envelope template {i}: shape', 'Sinc')
        gen.tooltip('The sinc wave will be defined from -x*PI to +x*PI')

        # Gaussian truncation
        gen.create_quant(f'Envelope template {i}: gaussian truncation', 'Truncate at x*sigma', 'DOUBLE', group, section)
        gen.default(2)
        gen.limits(low=1E-9)
        gen.visibility(f'Envelope template {i}: shape', 'Gaussian')

        # Duration Double
        gen.create_quant(f'Envelope template {i}: duration', 'Duration', 'DOUBLE', group, section)
        gen.unit('s')
        gen.visibility(f'Envelope template {i}: shape', *[j for j in TEMPLATES if j != 'Long drive'])
        gen.limits(low=1e-9, high=10E-6)
        gen.default(1e-9)

        # Padding settings
        gen.create_quant(f'Envelope template {i}: use zero-padding', 'Use zero-padding', 'BOOLEAN', group, section)
        gen.visibility(f'Envelope template {i}: shape', *[j for j in TEMPLATES if j != 'Long drive'])
        gen.tooltip('Lets you "shift" the template\'s start time by adding up to 2ns of leading zeroes to it.')

        gen.create_quant(f'Envelope template {i}: padding length', 'Padding length', 'DOUBLE', group, section)
        gen.unit('ns')
        gen.visibility(f'Envelope template {i}: use zero-padding', True)
        gen.limits(low=0, high=2)
        gen.default(1)
        gen.set_cmd('quarter_value')

        # Long drive special duration
        gen.create_quant(f'Envelope template {i}: long drive duration', 'Duration', 'STRING', group, section)
        gen.unit('s')
        gen.set_cmd('time_string', 'single')
        gen.tooltip('Example: 100E6 + 50E6*i')
        gen.default('0 + 0*i')
        gen.visibility(f'Envelope template {i}: shape', 'Long drive')

        # Gaussian rise and fall for long drive bool
        gen.create_quant(f'Envelope template {i}: use gaussian rise and fall', 'Use gaussian rise and fall', 'BOOLEAN', group, section)
        gen.visibility(f'Envelope template {i}: shape', 'Long drive')
        # Gaussian rise/fall duration
        gen.create_quant(f'Envelope template {i}: gaussian rise and fall duration', 'Rise and fall duration', 'DOUBLE', group, section)
        gen.tooltip('Both the rise and the fall have this duration, '
                    'and they are placed within the total duration of the pulse.')
        gen.limits(low=1e-9)
        gen.default(10e-9)
        gen.visibility(f'Envelope template {i}: use gaussian rise and fall', 'True')


def section_port_sequence(port):
    section = f'Port {port} sequence'
    group = 'General'

    # Whether to copy another sequence
    gen.create_quant(f'Port {port} - mode', 'Mode', 'COMBO', group, section)
    gen.combo_options('Disabled', 'Define', 'Copy', 'DRAG')

    gen.create_quant(f'Port {port} - copy sequence from', 'Copy from port', 'COMBO', group, section)
    gen.combo_options(*[str(i) for i in range(1, 9) if i != port])
    gen.visibility(f'Port {port} - mode', 'Copy')

    # DRAG options
    gen.create_quant(f'Port {port} - DRAG base', 'Base port', 'COMBO', group, section)
    gen.combo_options(*[str(i) for i in range(1, 9) if i != port])
    gen.visibility(f'Port {port} - mode', 'DRAG')

    # If we copy or use DRAG, add the option for phase shifting
    gen.create_quant(f'Port {port} - phase shift', 'Phase shift', 'DOUBLE', group, section)
    gen.unit('PI rad')
    gen.limits(-2, 2)
    gen.visibility(f'Port {port} - mode', 'Copy', 'DRAG')

    # If we copy, add the option for amplitude shifting
    gen.create_quant(f'Port {port} - amplitude scale shift', 'Amplitude scale shift', 'DOUBLE', group, section)
    gen.limits(-1, 1)
    gen.visibility(f'Port {port} - mode', 'Copy')

    gen.create_quant(f'Port {port} - DRAG scale', 'DRAG scale', 'DOUBLE', group, section)
    gen.default(1e-9)
    gen.unit('s')
    gen.visibility(f'Port {port} - mode', 'DRAG')

    gen.create_quant(f'Port {port} - detuning frequency', 'DRAG detuning frequency', 'DOUBLE', group, section)
    gen.unit('Hz')
    gen.limits(low=0)
    gen.visibility(f'Port {port} - mode', 'DRAG')

    # Number of groups to display
    gen.small_comment(f'Number of pulses for port {port}')
    gen.create_quant(f'Pulses for port {port}', 'Number of unique pulses', 'COMBO', group, section)
    gen.combo_options(*[str(i) for i in range(1, MAX_PULSE_DEFS+1)])
    gen.visibility(f'Port {port} - mode', 'Define')

    # Definition of individual pulses
    for i in range(1, MAX_PULSE_DEFS+1):
        group = f'Pulse definition {i}'

        # Template
        gen.create_quant(f'Port {port} - def {i} - template', 'Envelope', 'COMBO', group, section)
        gen.combo_options(*[str(j) for j in range(1, MAX_TEMPLATES+1)])
        gen.visibility(f'Pulses for port {port}', *[str(j) for j in range(i, MAX_PULSE_DEFS+1)])

        # Repeat
        gen.create_quant(f'Port {port} - def {i} - repeat count', 'Pulse repeat count', 'DOUBLE', group, section)
        gen.set_cmd('int')
        gen.default(1)
        gen.limits(low=1)
        gen.visibility(f'Pulses for port {port}', *[str(j) for j in range(i, MAX_PULSE_DEFS+1)])

        # Timing
        gen.create_quant(f'Port {port} - def {i} - start times', 'Start times', 'STRING', group, section)
        gen.set_cmd('time_string')
        gen.unit('s')
        gen.default('0 + 0*i')
        gen.tooltip('Example: 100E6 + 50E6*i, 700E6, ...')
        gen.visibility(f'Pulses for port {port}', *[str(j) for j in range(i, MAX_PULSE_DEFS+1)])

        # Choice of sine generator
        gen.create_quant(f'Port {port} - def {i} - sine generator', 'Sine generator', 'COMBO', group, section)
        gen.combo_options('1', '2', 'None')
        gen.visibility(f'Pulses for port {port}', *[str(j) for j in range(i, MAX_PULSE_DEFS+1)])

        # Sweep param
        gen.create_quant(f'Port {port} - def {i} - Sweep param', 'Sweepable parameter', 'COMBO', group, section)
        gen.combo_options('None', 'Amplitude scale', 'Carrier frequency', 'Phase')
        gen.visibility(f'Port {port} - def {i} - sine generator', '1', '2')

        # Params: amp
        gen.create_quant(f'Port {port} - def {i} - amp', 'Amplitude scale', 'DOUBLE', group, section)
        gen.limits(0, 1)
        gen.default(1)
        gen.visibility(f'Port {port} - def {i} - Sweep param', 'None', 'Carrier frequency', 'Phase')

        # Params: freq
        gen.create_quant(f'Port {port} - def {i} - freq', 'Carrier frequency', 'DOUBLE', group, section)
        gen.unit('Hz')
        gen.limits(0, 2E9)
        gen.visibility(f'Port {port} - def {i} - Sweep param', 'None', 'Amplitude scale', 'Phase')

        # Params: phase
        gen.create_quant(f'Port {port} - def {i} - phase', 'Phase', 'DOUBLE', group, section)
        gen.unit('PI rad')
        gen.limits(-2, 2)
        gen.visibility(f'Port {port} - def {i} - Sweep param', 'None', 'Amplitude scale', 'Carrier frequency')

        # How?
        gen.create_quant(f'Port {port} - def {i} - Sweep format', 'Sweep format', 'COMBO', group, section)
        gen.combo_options('Linear: Start-End', 'Linear: Center-Span', 'Custom')
        gen.visibility(f'Port {port} - def {i} - Sweep param', 'Amplitude scale', 'Carrier frequency', 'Phase')

        # Linear: Start-End
        gen.create_quant(f'Port {port} - def {i} - Sweep linear start', 'Start', 'DOUBLE', group, section)
        gen.visibility(f'Port {port} - def {i} - Sweep format', 'Linear: Start-End')
        gen.create_quant(f'Port {port} - def {i} - Sweep linear end', 'End', 'DOUBLE', group, section)
        gen.visibility(f'Port {port} - def {i} - Sweep format', 'Linear: Start-End')

        # Linear: Center-Span
        gen.create_quant(f'Port {port} - def {i} - Sweep linear center', 'Center', 'DOUBLE', group, section)
        gen.visibility(f'Port {port} - def {i} - Sweep format', 'Linear: Center-Span')
        gen.create_quant(f'Port {port} - def {i} - Sweep linear span', 'Span', 'DOUBLE', group, section)
        gen.visibility(f'Port {port} - def {i} - Sweep format', 'Linear: Center-Span')

        # Custom steps
        gen.create_quant(f'Port {port} - def {i} - Sweep custom steps', 'Step values', 'STRING', group, section)
        gen.tooltip('Separate with comma')
        gen.set_cmd('double_list')
        gen.visibility(f'Port {port} - def {i} - Sweep format', 'Custom')


def section_sample():
    section = 'Sampling'
    group = 'Timing'

    # Timings
    gen.create_quant(f'Sampling - start times', 'Start times', 'STRING', group, section)
    gen.set_cmd('time_string')
    gen.unit('s')
    gen.default('0 + 0*i')
    gen.tooltip('Example: 100E6 + 50E6*i, 700E6, ...')

    # Duration
    gen.create_quant('Sampling - duration', 'Duration', 'DOUBLE', group, section)
    gen.limits(0, 4096E-9)
    gen.unit('s')

    group = 'Port selection'
    # Port selection
    for i in range(1, 9):
        gen.create_quant(f'Sampling on port {i}', f'Port {i}', 'BOOLEAN', group, section)

    # Result values (readonly vectors, so they aren't visible)
    for i in range(1, 9):
        gen.create_quant(f'Port {i}: Time trace', '', 'VECTOR', group, section)
        gen.get_cmd('get_result')
        gen.add_line('x_unit: s')
        gen.visibility(f'Sampling on port {i}', True)
        gen.show_in_measurement(True)

    # Custom template input vectors
    for i in range(1, CUSTOM_TEMPLATES + 1):
        gen.create_quant(f'Custom template {i}', '', 'VECTOR', group, section)
        gen.permission('WRITE')

    # Template previews
    for template in range(1, MAX_TEMPLATES+1):
        gen.create_quant(f'Template {template}: Preview', '', 'VECTOR', group, section)
        gen.get_cmd('template_preview')
        gen.add_line('x_unit: s')
        gen.visibility(f'Envelope template {template}: shape', *TEMPLATES)


def section_preview():
    section = 'Preview'
    group = 'Settings'

    gen.create_quant('Preview port', 'Preview sequence on port', 'COMBO', group, section)
    gen.combo_options(*[i for i in range(1, 9)])

    gen.create_quant('Preview iteration', 'Preview iteration', 'DOUBLE', group, section)
    gen.default(1)
    gen.limits(low=1)
    gen.set_cmd('int')

    gen.create_quant('Enable preview slicing', 'Enable preview slicing', 'BOOLEAN', group, section)
    gen.tooltip('This will let you specify which segment of the pulse sequence to preview.')

    gen.create_quant('Preview slice start', 'Slice start', 'DOUBLE', group, section)
    gen.unit('s')
    gen.limits(low=0)
    gen.visibility('Enable preview slicing', True)

    gen.create_quant('Preview slice end', 'Slice end', 'DOUBLE', group, section)
    gen.unit('s')
    gen.limits(low=1E-9)
    gen.default(1E-9)
    gen.visibility('Enable preview slicing', True)

    gen.create_quant('Preview sample windows', 'Preview sample windows', 'BOOLEAN', group, section)
    gen.tooltip('This will display sample windows as flat lines at y=-0.1. '
                'Pulses that overlap with these sample windows will be hidden.')

    gen.create_quant('Pulse sequence preview', '', 'VECTOR', group, section)
    gen.permission('READ')


########## INIT ##########
gen.general_settings(NAME, VERSION, DRIVER_PATH, author='Johan Blomberg and Gustav Grännsjö', interface=INTERFACE)

# TEMPLATES
gen.big_comment('TEMPLATES')
section_templates()

gen.big_comment('SWEEPABLE PULSE (and more...)')
section_general()

for p in range(1, 9):
    gen.big_comment(f'Pulse definitions - Port {p}')
    section_port_sequence(p)

gen.big_comment('SAMPLING')
section_sample()

gen.big_comment('PREVIEW')
section_preview()

gen.write(FILENAME)
