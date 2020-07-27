# GUI
The GUI is sorted into multiple files, prefixed with "gui_" and located in the gui subfolder. You can move them out of this folder into the game directory if you want.

- removed gui variables that were useless (i.e. defined and used for usully only one property), kept the ones that were used to conditionally use one UI element over another. Comments specify Ren'Py's suggested mobile alternatives and what other property a style value inherited from, if any (for example, sometimes xmaximum was set to match xsize)
- this project assumes you won't likely be making a game for mobile AND desktop
- code has a tendency to specify both text_align and xalign to the same value, same with xsize and xmaximum/xminimum, even though according to docs both of these are redundant?

## File Structure
- ***gui_nav.rpy*** contains screens used to access and configure the game.
  - Main menu
  - Game menu
  - Shared "navigation" buttons used by both
- ***gui_advnvl.rpy*** contains screens used in the main gameplay loop.
  - ADV mode/choices screens
  - NVL mode/choices screens
  - Input screen
  - Quick menu
- ***gui_hud.rpy*** contains simple, single-purpose screens and indicators that appear on top of other screens, usually on top of the main game flow.
  - Skip indicator
  - Yes/No screen
  - Notification popup
- ***gui_prefs.rpy*** separates the options screen to avoid cluttering up *gui_nav.rpy*.
  - Preferences screen
- ***gui_extras.rpy*** contains screens with modular "bonus" game features, usually accessible from the main menu.
  - Web updater screen
  - CG gallery
  - Music room
  - Scene/replay select

## Custom Actions (*module_actions.rpy*)

### `Increment()`
These are used to increase or decrease a value using buttons. For example, you could place an imagebutton, with "plus" and "minus" signs, on either side of a volume slider, and give them the `Increment()` action to create buttons that will increase or decrease the volume, like this:

```
textbutton "-" action Increment("music volume", decrease=True)
bar value Preference("music volume")
textbutton "+" action Increment("music volume")
```

Where "music volume" is the name of the preference to adjust, as a string. It can also be a field in the persistent object (ex: "something" would adjust persistent.something). To adjust a general, non-persistent variable, add `store=store` to the parameters. The value of this variable should be

Set **decrease** to True on the minus or back-facing button, to decrease the value.

With volume sliders, the value will adjust by increments of .25 (out of a max value of 1.0 for 100% volume). To adjust this, or to specify the correct increment and range values for another variable or preference setting, use the **step** and **max** parameters.

Putting it all together, an in-game screen might look like this:

```
default persistent.candies = 10

screen candyTime():
  vbox:
    text _("How many candies should I give them?")

    hbox:
      textbutton "-" action Increment("candies", decrease=True, step=5, max=20)
      label str(candies)
      textbutton "+" action Increment("candies", step=5, max=20)
```

### `IncrementList()`

This is a wrapper for `Increment()` which offers list functionality (you could also call `Increment()` with a **list** parameter). If you have a list of options you want the user to be able to click through using forward/back arrows, you could use something like this:

```
define hats = [_("Trilby"), _("Party Hat"), _("Rasta Cap"), _("Tiny Steampunk Hat")]
default persistent.playerHat = hats[0]

screen hatPicker():
  text _("Choose a hat to wear.")

  textbutton "<" action IncrementList("playerHat", hats, decrease=True)
  label persistent.playerHat
  textbutton ">" action IncrementList("playerHat", hats)
```
