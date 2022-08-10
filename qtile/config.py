# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook
from widgets.spotify import Spotify
import os
import subprocess
from qtile_extras import widget

mod = "mod4"
terminal = "kitty"
browser = "firefox"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Spawn a command using a prompt widget"),
    Key([mod], "b", lazy.spawn(browser), desc="Spawn browser"),
    Key([], "Print", lazy.spawn("flameshot gui")),
    Key([mod], "p", lazy.spawn("xscreensaver-command -lock")),
]

groups = [Group(i) for i in "爵ﴬﭮ78"]

for num, group in enumerate(groups, 1):
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                str(num),
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                str(num),
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ])

layouts = [
    layout.Columns(border_normal="301934", border_focus="#512da7", border_width=2, margin=9),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
     layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
     layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="agave regular Nerd Font",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# Edges of widgets to give them style
def borderSlopeL(foreground, background):
    return widget.TextBox("\ue0bc", foreground=foreground, background=background, font="Inconsolata for powerline", fontsize=33, padding=0)

def borderSlopeR(foreground, background):
    return widget.TextBox("\ue0be", foreground=foreground, background=background, font="Inconsolata for powerline", fontsize=33, padding=0)

def borderTriangleL(foreground, background):
    return widget.TextBox("\ue0b2", foreground=foreground, background=background, font="Inconsolata for powerline", fontsize=33, padding=0)

def borderTriangleR(foreground, background):
    return widget.TextBox("\ue0b0", foreground=foreground, background=background, font="Inconsolata for powerline", fontsize=33, padding=0)

def borderCircleL(foreground, background):
    return widget.TextBox("\u25d6", foreground=foreground, background=background, font="Inconsolata for powerline", fontsize=33, padding=0)

def borderCircleR(foreground, background):
    return widget.TextBox("\u25d7", foreground=foreground, background=background, font="Inconsolata for powerline", fontsize=33, padding=0)


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(background="b19cd9", font="HeavyData Nerd Font"),
                Spotify(foreground="00ff22"),
                #widget.Prompt(),
                widget.Spacer(),
                widget.Systray(),
                borderTriangleL("816797", None),
                widget.TextBox("", font="HeavyData Nerd Font", background="816797"),
                widget.CPU(format="{freq_current}GHz {load_percent}%", background="816797"),
                borderTriangleL("51557E", "816797"),
                
                widget.TextBox("", font="HeavyData Nerd Font", background="51557E"),
                widget.Memory(background="51557E"),
                #widget.DF(visible_on_warn=False),
                borderTriangleL("19456B", "51557E"),
                widget.TextBox("墳", font="HeavyData Nerd Font", background="19456B"),
                widget.Volume(fmt="{}", background="19456B"),
                borderTriangleL("11698E", "19456B"),
                widget.TextBox(" ", font="HeavyData Nerd Font", background="11698E"),
                widget.Wlan(format="{essid} {percent:2.0%}", interface="wlp3s0", background="11698E"),
                
                widget.TextBox("", font="HeavyData Nerd Font", background="0075b3"),
                widget.Bluetooth(hci="/dev_E8_EC_A3_C7_71_F4", background="0075b3"),
                
                borderTriangleL("0C907D", "0075b3"),
                widget.Battery(charge_char= "",
                discharge_char= "",
                full_char= "",
                empty_char= "",
                unknown_char= "",
                low_percentage= 0.3,
                format= "{char} {percent:2.0%}",
                background="0C907D"),
                
                borderTriangleL("12CC94", "0C907D"),
                widget.Clock(format="%I:%M %p %d-%m", fontsize=12, background="12CC94"),
            ],
            24,
            margin = [9, 9, 2, 9]

            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/scripts/autostart.sh'])
