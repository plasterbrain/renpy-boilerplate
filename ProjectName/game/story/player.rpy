################################################################################
## Story: Player Object
################################################################################
## This is a basic player class you can use to handle inventories of any sort.
## You could also send choice-related data to it to avoid cluttering up the
## global namespace.

init python:
    import renpy.store as store
    import renpy.exports as renpy

    class Player(renpy.store.object):
        def __init__(self):
            self.items = {}
            self.choices = {}
