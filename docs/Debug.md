# Debug Settings and Tools (*dev/*)
This is your toolkit for testing your game.

## How to use this file
There are some keymap settings in here that you probably don't need to change.

```
renpy "{THING}" lint "lint.txt"
```

### Auto-play
This is a group of functions and settings which can be used to make your game play itself, either as a demonstration (e.g. at conventions) whether your game functions, on a surface level, from start to finish. In the latter case, the command is especially helpful if you have multiple routes that would otherwise require several manual playthroughs.

```
renpy "{PATH TO PROJECT}" auto --route "chris";
```

Depending on how unique your visual novel is -- for example, if it has QTEs, you may need to write code to determine how auto mode reacts in special cases.

For example, you can use the `is_automode` variable to conditionally dismiss screens that would otherwise wait for user input, adding something like:

```
    if is_automode:
        timer 0.5 action Return()
```

`renpy.queue_event()` is another useful tool. It simulates the given `config.keymap` action, as though the user pressed the keys to trigger it.

Auto mode will pick a menu option for in-game choices at random. If some of these might lead to game overs, for example, and you don't want that to stop the game forever, you can create a function for `config.label_callback` (or update the existing one if it exists) to handle getting out of certain labels.

By setting `config.autosave_on_choice` to True in the auto function and creating a label callback like this:

```python
  def label_test_callback(name, jumped):
      if name == "gameover":
          renpy.load(renpy.newest_slot())
```

we can simply reload the last choice and try again until the script picks a non-gameover choice.
