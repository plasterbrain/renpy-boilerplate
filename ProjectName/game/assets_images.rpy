################################################################################
## Displayables
################################################################################
## Definitions for special images, animations, transforms, and transitions.

## -- Display Settings ---------------------------------------------------------

init python:

    ## --- FPS
    config.framerate = 100

    ## --- Nearest Neighbor Interpolation
    ## For games using pixel art.
    config.nearest_neighbor = False

    ## --- Default Shader
    ## Default Ren'Py shaders include renpy.geometry, renpy.texture,
    ## renpy.solid, renpy.dissolve, renpy.imagedissolve, renpy.colormatrix,
    ## renpy.alpha, and renpy.ftl.
    config.default_shader = "renpy.geometry"

    ## --- Custom Show Statements
    ## Functions used in place of Ren'Py's built in show, hide, and scene
    ## functions. These should have the same signature as the originals.
    config.show = renpy.show
    config.hide = renpy.hide
    config.scene = renpy.scene

    ## --- Displayable Prefixes
    ## https://www.renpy.org/doc/html/displayables.html#displayable-prefix
    ## Dictionary mapping prefixes to functions used to transform displayables.
    # config.displayable_prefix[] = None

## -- Layers -------------------------------------------------------------------
## Layers are used for both images and screens.

init python:

    ## --- Layer List
    ## List of displayable layers in z-index order. This should always contain
    ## at least "master", "transient", "screens", and "overlay."
    config.layers = ["master", "transient", "screens", "overlay"]

    ## --- Layer List (Top)
    ## List of names of layers that are displayed above all other layers, and do
    ## not participate in a transition that is applied to all layers. If a layer
    ## name is listed here, it should not be listed in config.layers.
    config.top_layers = []

    ## --- Transient Layers
    ## List of all of the transient layers. Transient layers are layers that are
    ## cleared after each interaction. "transient" should be in this list.
    config.transient_layers = ["transient"]

    ## --- Overlay Layers
    ## List of all of the overlay layers. Overlay layers are cleared before the
    ## overlay functions are called. "overlay" should be in this list.
    config.overlay_layers = ["overlay"]

    ## --- Layer Clipping
    ## A map of layer names to (x, y, height, width) tuples, where x and y are
    ## the coordinates of the upper-left corner of the layer, with height and
    ## width giving the layer size.
    # config.layer_clipping = {}

    ## --- Default Image Layer
    config.default_tag_layer = "master"

    ## A dictionary mapping image tags to their preferred layer.
    config.tag_layer = {}

    ## A dictionary mapping image tags to their preferred zorder value.
    config.tag_zorder = {}

## -- Images -------------------------------------------------------------------

init python:

    ## --- Missing Images
    ## Function called when an attempt to load an image fails. It may return
    ## None, or it may return an image manipulator. If an image manipulator is
    ## returned, that image manipulator is loaded in place of the missing image.
    # config.missing_image_callback = None

    ## Function used when a show statement calls an image that can't be found.
    ## It accepts three parameters: the image name to be shown (as a string), an
    ## optional "what" parameter (used in show expression statements) that
    ## resolves to a displayable, and the layer to show the image on (a string).
    ## The function should return a displayable.
    ##
    ## Because scene statements also call renpy.show after clearing the layer,
    ## this callback is used for both show and scene statements, and would be
    ## called after config.missing_scene.
    # config.missing_show = None

    ## Function used when a hide statement calls an image that can't be found.
    ## It accepts two parameters: the image name to hide (a string), and the
    ## layer to remove the image from (a string). You might use it to clean up
    ## any anomalies introduced with the missing_show callback.
    # config.missing_hide = None

    ## Function used when a scene statement calls an image that can't be found.
    ## It accepts one parameter, the name of the layer to clear (a string).
    # config.missing_scene = None

    ## Image attribute, as a string, to be added to a character's image tag when
    ## that character is speaking, and removed when the character stops.
    config.speaking_attribute = None

## Define images that weren't automatically declared here!

define _anim_load = "gui/anim/loading/load-%d.png"

image load_icon:
    _anim_load % 1
    0.1
    _anim_load % 2
    0.1
    _anim_load % 3
    0.1
    _anim_load % 4
    0.1
    _anim_load % 5
    0.1
    _anim_load % 6
    0.1
    _anim_load % 7
    0.1
    _anim_load % 8
    0.1
    repeat

## -- Movies -------------------------------------------------------------------

init python:

    ## --- Movie Replay (7.0)
    ## Whether showing a movie sprite already on screen restarts the movie.
    config.replay_movie_sprites = True

## Define movies here!

#-- Transforms -----------------------------------------------------------------

init python:

    ## When a displayable is shown using the show or scene statements, the
    ## transform properties are taken from this transform and used to initialize
    ## the values of the displayable's transform.
    config.default_transform = center

    ## A dictionary mapping image tag strings to transforms (or lists of
    ## transforms). When an image is newly-shown without an at clause, it will
    ## be shown using the default transform(s) given in this dictionary.
    config.tag_transform = {}

    ## --- Inherit Child Position (6.11.0)
    ## Whether transforms inherit position properties from their child.
    config.transform_uses_child_position = True

    ## --- Continue ATL Transforms (6.12.1)
    ## If True, showing an image without supplying a transform or ATL block will
    ## cause the image to continue the previous transform being used by an image
    ## with that tag, if any. If False, the transform is stopped.
    config.keep_running_transform = True

    ## --- Persist Show Layer State (6.99.13)
    ## Whether the show layer at statement persists the state of a transform
    ## like any other ATL transform.
    config.keep_show_layer_state = True

    ## Whether the at list is sticky.
    config.sticky_positions = False

    ## Whether Ren'Py wraps shown transforms in an `ImageReference` object.
    config.wrap_shown_transforms = True

    ## Whether ATL automatically causes polar motion for angle changes.
    config.automatic_polar_motion = True

## -- Transitions --------------------------------------------------------------

init python:

    ## --- (Callback) With Statement
    ## Function that is called when a "with" statement occurs. It accepts a
    ## single argument, the transition that is occurring. It should return a
    ## transition, which may or may not be the one it was given.
    config.with_callback = None

    ## --- Force Alpha (7.0)
    ## Whether Dissolve(), ImageDissolve(), and AlphaDissolve() transitions use
    ## the alpha channel of the source displayables, as if alpha=True was given.
    config.dissolve_force_alpha = True

    ## Whether MoveTransition() takes offsets into account.
    config.movetransition_respects_offsets = True

## Define transitions here!
