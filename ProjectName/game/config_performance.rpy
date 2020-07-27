################################################################################
## Configuration: Performance/Graphics Settings
################################################################################
## Settings to control how Ren'Py renders and optimizes graphics and screens.

## -- Caching ------------------------------------------------------------------

init python:

    ## --- Image Surface Cache (6.99.13)
    ## Whether the underlying data of an image is stored in RAM, allowing image
    ## manipulators to be applied to that image without reloading it from disk.
    ## If False, the data is dropped from the cache, but kept as a texture in
    ## video memory, reducing RAM usage of the image cache by about half.
    config.cache_surfaces = False

    ## --- Image Cache Size (Screens)
    ## The size of the image cache, as a multiple of the screen size in pixels.
    config.image_cache_size = None

    ## --- Image Cache Size (MB)
    ## Used if image_cache_size is None. Each image takes 4 bytes per pixel, or
    ## 8 bytes per pixel if `config.cache_surfaces` is enabled.
    config.image_cache_size_mb = 300

    ## --- Imagemap Cache
    ## If True, imagemap hotspots will be cached to PNG files, reducing time and
    ## memory usage, but increasing the size of the game on disk.
    config.imagemap_cache = True

    ## --- Screen Cache
    ## The number of copies of each screen to keep in the screen cache.
    config.screen_cache_size = 4

## -- Optimization -------------------------------------------------------------

init python:

    ## --- Font Preloading
    ## A list of TrueType and OpenType font names that Ren'Py should load when
    ## starting up. Though this may increase startup time, including fonts here
    ## may prevent Ren'Py from pausing when introducing them in-game.
    config.preload_fonts = []

    ## --- List Compression
    ## How many elements should be in a list before we compress it for rollback.
    config.list_compression_length = 25

    ## --- Optimize Image Loading (6.99.14.1)
    ## When True, Ren'Py will scan images to find the bounding box of the non-
    ## transparent pixels, and only load those pixels into a texture.
    config.optimize_texture_bounds = True

## -- Prediction ---------------------------------------------------------------

init python:

    ## --- Condition Switch Prediction
    ## The default value used when the predict_all argument for a
    ## ConditionSwitch() or ShowingSwitch() displayable is set to None.
    config.conditionswitch_predict_all = False

    ## --- Image Prediction
    ## Number of statements, including the current one, to consider when doing
    ## predictive image loading. A breadth-first search from the current
    ## statement is performed until this number of statements is considered, and
    ## any image referenced in those statements is potentially predictively
    ## loaded. Set this to 0 to disable image prediction.
    config.predict_statements = 10

    ## --- (Callbacks) Image Prediction
    ## Functions called, without arguments, when predicting images.
    # config.predict_callbacks.append()

    ## --- Screen Prediction
    config.predict_screens = True

    ## Predict file pages on save/load screen
    config.predict_file_pages = True

    ## --- (Callback) Statement Prediction
    ## Function that returns a list of statement identifiers that should be
    ## predicted. It is called with one argument, the current statement id.
    # config.predict_statements_callback = None

## -- Rendering ----------------------------------------------------------------

init python:

    ## --- (Mobile) Hardware Video Playback
    ## Whether to use hardware video on supported mobile platforms.
    config.hw_video = False

    ## --- OpenGL 2 (7.4.0)
    ## Whether to enable and require GL2.
    # config.gl2 = True

    ## --- OpenGL Acceleration
    ## Whether to use OpenGL acceleration. Note that this will automatically be
    ## disabled if it's determined that the system cannot support it.
    ## OpenGL can also be disabled by holding down shift at startup.
    config.gl_enable = True

    ## --- OpenGL Depth Buffer
    ## Bits of depth the game should use, if any.
    config.depth_size = None

## -- Garbage Collection -------------------------------------------------------

init python:

    ## Whether Ren'Py manages the Python garbage collector
    config.manage_gc = True

    ## The GC thresholds that Ren'Py uses when not idle. These are set to try
    ## to ensure that garbage collection doesn't happen. The three numbers are:
    config.gc_thresholds = (25000, 10, 10)

    ## The net number of objects that triggers a collection when Ren'Py has
    ## reached a steady state.
    config.idle_gc_count = 2500
