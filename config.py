import os
import subprocess
from typing import List
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"
terminal = "alacritty"
browser = 'brave'
file_manger = 'pcmanfm'

keys = [

    # Switch between windows
    Key([mod], "h",
        lazy.layout.left(),
        desc="Move focus to left"
        ),
    Key([mod], "l",
        lazy.layout.right(),
        desc="Move focus to right"
        ),
    Key([mod], "j",
        lazy.layout.down(),
        desc="Move focus down"
        ),
    Key([mod], "k",
        lazy.layout.up(),
        desc="Move focus up"
        ),
    Key([mod], "space",
        lazy.layout.next(),
        desc="Move window focus to other window"
        ),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        desc="Move window to the left"
        ),
    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right"
        ),
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        desc="Move window down"
        ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        desc="Move window up"
        ),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        desc="Grow window to the left"
        ),
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        desc="Grow window to the right"
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        desc="Grow window down"
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        desc="Grow window up"
        ),
    Key([mod], "n",
        lazy.layout.normalize(),
        desc="Reset all window sizes"
        ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    Key([mod], "b", lazy.spawn(browser)),
    Key([mod], "e", lazy.spawn(file_manger)),

    Key([mod, "shift"], "Return", lazy.spawn('dmenu_run'),
        desc="Spawn a command using a prompt widget"),

    Key([mod], "Right", lazy.screen.next_group()),
    Key([mod], "Left", lazy.screen.prev_group()),
]

groups = []

group_labels = ['爵', '', '', '', '', 'ﱘ']
group_names = [str(i) for i in range(1, len(group_labels)+1)]

for i in range(len(group_names)):

    group = Group(
        name=group_names[i],
        layout='MonadTall',
        label=group_labels[i]
    )

    groups.append(group)

    keys.extend([
        Key([mod], group.name,
            lazy.group[group.name].toscreen(),
            desc="Switch to group {}".format(group.name),
            ),
        Key([mod, "shift"], group.name,
            lazy.window.togroup(group.name),
            desc="Switch to & move focused window to group {}".format(
                group.name),
            )
    ])

colors = {
    'bg': '#1d2021',
    'white': '#ffffff',
    'red': '#cc241d',
    'green': '#98971a',
    'yellow': '#fabd2f',
    'blue': '#458588',
    'purple': '#8f3f71',
    'aqua': '#689d6a',
    'orange': '#d65d0e',
}

layouts = [
    layout.MonadTall(
        border_focus=colors['red'],
        margin=10,
    ),
    layout.Max(),
]

widget_defaults = dict(
    font='Hack Nerd Font',
    fontsize=16,
    padding=10,
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    rounded=False,
                    active=colors['yellow'],
                    inactive=colors['white'],
                    highlight_method="line",
                    this_current_screen_border=colors['green'],
                    padding=8,
                ),
                widget.Prompt(),
                widget.Spacer(length=bar.STRETCH),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.CurrentLayout(
                    background=colors['red'],
                ),
                widget.Memory(
                    format='{MemUsed: .0f}{mm}',
                    background=colors['purple'],
                ),
                widget.Battery(
                    background=colors['orange'],
                    charge_char='',
                    discharge_char='',
                    font='Hack Nerd Font',
                    format='{char}{percent: 1.0%}',
                ),
                widget.Clock(
                    format='%I:%M %p',
                    background=colors['blue'],
                ),
                widget.Clock(
                    format='%a %d-%m-%y',
                    background=colors['aqua'],
                ),
            ],
            25,
            background=colors['bg']
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# startup apps


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
