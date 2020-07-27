# Preferences

Init blocks with `in increments` are used to define lists of options the user can choose from for each preference. They're needed for the `IncrementList()` action, which lets the user press a "next" or "previous" arrow option to rotate through various options.

The items in these lists will also have corresponding names defined in *gui_prefs.rpy*. Check them out to get a better idea of what the various option values actually mean.

The general init blocks are used for config variables and the like, which are used to set certain defaults, affect certain preference parameters outside of player control, create custom preferences, and determine which gameplay features and options are even available.

Finally, there's a series of `default` statements, to set the default value of preferences the user will be able to change. Most are marked with the "## ---!" indicator. This is because registering them with a `default` statement stores their default values in `persistent._preference_default`, which is used to provide the "reset preferences" utility function. If you delete a default declaration, the corresponding variable cannot be reset to its default value by `_delete_prefs()`.

### Advanced users only

#### Compatibility garbage

- `config.default_language` seems to be an unnecessary duplicate of `config.language`.

## The keymap

Some keymap terminology:
- **Event:** Pygame instances of captured input, such as clicking a mouse, moving a joystick, or pressing one or more keyboard keys.
  - The "down" and "up" components of clicks and keypresses are separate events.
- **Action:** The various keys in the config.keymap dictionary, like "rollback" or "toggle_afm." The Ren'Py docs also refer to these as "events" once or twice, but we'll avoid this to distinguish them from Pygame events.
- **Keysym:** Strings used to reference input events, most notably in `config.keymap` and by using the `key` statement on Ren'Py screens.
  - Pygame/SDL2 keysyms are constants beginning with "K_", representing keyboard and some Android* events.
  - Ren'Py keysyms are more human-readable strings representing mouse, joystick/gamepad, Android and keyboard events. With Pygame, something like "left shift + right alt + P" would be stored as an event object, with a "key" attribute representing K_p, and a "mod" attribute that's a bitmask integer representing the shift and alt keys. In Ren'Py, this can all be represented as a single string, "alt_shift_K_p".
- **Keycode:** This is an arbitrary name I use in the code to refer to Ren'Py-style keysyms just to differentiate between the two. "keysym" will usually refer to Pygame constants.
- **Modifier:** Certain keys are allowed to be coupled with other keysyms. For example, you can't bind an action to the event of pressing J, A, and M all at the same time, but you can couple any one of those keys with one or more modifiers.
  - Ren'Py accepts the following Pygame modifiers: "shift", "ctrl", "alt", and "meta" (the Windows or command key, `K_GUI`). It stores some other event properties as modifiers, though they aren't considered modifier "keys" by Pygame. These are "keydown" (key is being pressed, assumed by default), "keyup" (key is being released), and "repeat" (key is being held down).
  - When used as modifiers, Ren'Py views the left/right versions of a modifier (like `K_LSHIFT` and `K_RSHIFT`) as the same key.
  - Pygame modifier keys can be used as input events by themselves. In this case, the position of the modifier becomes relevant. (ex. An event could be triggered by right ctrl but not left ctrl.)

\*"K_AC_BACK" is listed as the "Android back button" in [this rapt pygame example](https://github.com/renpytom/rapt-pygame-example/blob/dcc43e790d8fef0fcc1d1d81887bf1c68e7bdb24/main.py). There are actually more keys with the "K_AC_" prefix that presumably belong to Androids: SEARCH, HOME, FORWARD, STOP, REFRESH, and BOOKMARKS.

### Getting human-readable keynames

`get_keyname_from_keycode()` can generate a human-readable name from an arbitrary Ren'Py keycode. It assumes your keycodes follow the correct format:
  1. Modifier prefixes are at the beginning of the string.
  1. Prefixes are separated by underscores.
  1. Only one non-modifier key exists.

If you don't do this your video game will explode.

### Creating rebindable keys with `KeymapAction()`
This custom keybindings feature is accomplished by creating a KeymapAction object for each action (the dict keys of `config.keymap`), and then adding up to one bindable key "slot" to it using `add_slot()`, and an arbitrary number of "frozen" keys using `add_frozen()`

This has already been done for you in *module_keymap.rpy*, so all you have to do is edit the values.

To remove a predefined action from your game entirely, don't bother making an object for it. Just set its `config.keymap` value to an empty list.

#### Key considerations
By default, the "enter" event group has "z" as a rebindable key. This is because the enter key, while a tempting rebindable candidate, is also used  by "input_enter" (aka, submitting text the user types in).

"input_enter" is a tricky one to rebind, because almost any other key (letters, shift, or space) would either cause many players to accidentally end the input early or are nonsensical.

If you want the enter key to be rebindable, your game should either not use text input events, have an on-screen keyboard and/or submit button, or use an unusual frozen key event for input enter (like enter + shift) that is mentioned in the input prompt (like "What is your name? Press Shift + Enter when you're ready to submit").

Similarly, the escape key is frozen to "game_menu" by default. It's a useful permanent binding to have, as it's used to exit the in-game developer console, which is a lot like input events. Furthermore, it allows us to reserve the escape key as a way for keyboard users to cancel key binding. (Mouse users can just click.)

"game_menu" has an unused open slot to start. Note that, as mentioned, the "game_menu" action is used to exit the developer console, so you should avoid setting it to a regular alphanumeric key. This probably won't be an issue for players (@TODO or IS IT? re: input???).

### Compatibility: Joysticks
I don't have an exact patch number, but Ren'Py's support for joysticks (that is, DirectInput controllers) has been deprecated in favor of gamepads (XInput controllers). You can still find some config variables and compatibility screens lying around. You can write a screen to replace `joystick_preferences_screen()` and call it from the preferences menu, and set the following variables:

- `config.joystick` - Whether the game should try to support joysticks.
- `preferences.joymap` - A dictionary mapping synthetic keys to joystick events (I think).
- `config.joystick_keys` - A list of tuples pairing human-readable names with synthetic joystick keys. It looks like this:
```python
config.joystick_keys = [
      (_("Left"), 'joy_left'),
      (_("Right"), 'joy_right'),
      (_("Up"), 'joy_up'),
      (_("Down"), 'joy_down'),
      (_("Advance text"), 'joy_dismiss'),
      (_("Rollback"), 'joy_rollback'),
      (_("Skip"), 'joy_holdskip'),
      (_("Toggle skipping"), 'joy_toggleskip'),
      (_("Hide interface"), 'joy_hide'),
      (_("Pause"), 'joy_menu')]
```
