The scene select list auto-populates. Built-in special labels (or the labels you replaced them with in `config.label_overrides`) are ignored, as well as labels with "\_screen" in the name (which Ren'Py uses as a fallback for certain built-in screens) and labels starting with an underscore.

The scenes in the list are represented by a tuple containing the human-readable scene name and then the corresponding script label.

To get a human-readable name for a scene to show in the menu, the script looks for the scene label name in `scene_names`, which you can use to specify custom names (such as \__("Chapter 1: What It Means") for an ugly label like "hl2ql_ch1_start"). If no name is supplied, the default name will be the label name, capitalized, with underscores replaced by spaces. This auto-generated name is not translateable, so you should add custom names if you plan on including multiple languages.

By default, the list of scenes is ordered naturally by label name, to give you the opportunity to choose their order through label names, regardless of whether their human-readable names are alphabetical.

Obviously, this setup will not work for all visual novels, especially when scenes can be affected by variables set earlier in the game. But, by building on this basic structure, you can add additional fields to the scene list or structure scenes under sub-headings (like for chapters or routes).

The scene select menu uses `Replay()` by default.

Features of `Replay()`:
- Used to revisit a single scene
- Scenes go until a `renpy.end_replay()` flag is reached, then return the user to wherever they started the replay from.
- (+) Easier to scope variables to replay-only values
- (-) Saving is disabled.

Features of `Start()`:
- Used to start the game from a certain point
- Scenes go until reaching a `return` statement at the end of the call stack.
- (-) Only works from the main menu\*
- (-) You'll need to find a way to set any variables that affect how the game progresses.
- (+) Does not affect saving.

\*By default, the scene select screen is only accessible from the main menu, though developers can also access it through the game menu for easier testing. While it is perhaps possible to accomplish a game menu scene select using `Jump()`, for non-kinetic games, it will make scoping variables even more complex.
