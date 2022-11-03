# SquashTex

Squash a multi-file LaTeX project into one main file.

Run with `python squashtex.py directory_name mainfile_name outputdirectory_name`. Only the first arguments is required, and it should be the path to the directory where you LaTeX project is. The second argument defaults to `mainfile_name = main`, and the third argument defaults to `outputdirectory_name = squashed_output`. The resulting squashed project (with all comments removed) will be in the directory `directory_name/outputdirectory_name`.
