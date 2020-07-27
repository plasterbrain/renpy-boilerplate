################################################################################
## Developer: Debug Room
################################################################################
## A place to test screens and other code without affecting the actual script.

label debug_room:
    if not config.developer:
        jump start
    scene bg toy night
    show molly base neutral at left with easeinleft
    menu:
        "What do you want to see?"
        "nothing":
            pass
    e "This is a character speaking."
    "This is a narrator speaking."
    e "The itch.io update screen looks like this!"
    show screen itch_update_prompt()
    e "The error screen looks like this..."
    $ eggs.get("")
    e "Here's the performance warning screen that users may get on startup."
    call screen _performance_warning("sw")
    "This is an input:"
    $ renpy.input(_("What's your name?"))
    menu:
        "Here's a menu!"
        "Agree":
            "You agreed with the menu."
        "Disagree":
            e "Screw this menu. I wanted a kinetic novel."
    en "Now it's novel time, the part of the debug room where the text takes up the whole screen."
    en "Ah, the novel screen. The swiss army knife for devs when they realize they chose the wrong medium for their prose."
    en "\"I can't draw enough pictures to describe all this,\" cries the developer. \"I would need like thirty CGs.\""
    en "She hopes the reader will forget they are playing a visual novel."
    en "Maybe they will just assume it's Kindle!"
    $ eggs.get("")
    en "I suppose I'm not being fair. The priciest Ren'Py games get is like $25, compared to a $30-40 Japanese visual novel."
    en "That's about the price of a new hardcover book."
    en "It is! I have Barnes and Noble's top-selling books open right here. The number one has an MSRP of $28!"
    en "Even if one were to write an entire visual novel in novel mode, it's still probably going to have some sounds and more pictures than a hardcover book."
    en "To say nothing of programming!"
    en "I'm sorry, but while I don't know much about typesetting, it cannot be more difficult than learning Python."
    en "The point is, visual novels are quite the bargain."
    nvl clear
    en "Time to clear the screen."
    e "Anyway, that's all I have to say about visual novels. Let's go back to the main menu!"
    return
