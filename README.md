# file-revision
Small script to revise file names based on dependencies

# Run
Using the `makefile` will allow you to run both the revision app using:

`make run`

or the tests:

`make test`

# Context
Current version uses a `directory_path` argument passed to the `main` function in the `revision.py` script. A relative default path has been set for the current directory as found in the repo. 
This can be overriden in the script using an absolute path if the files are outside of the `revision_app` directory, or relative if within.

The script requires no additional requirements to be installed and will work with `Python 3.9` onwards.

# Note
The brief indicates 3 unique parameters (name, revises_id, and revision_id). In the given files the revision_id fields and the filename are identical, save a file extenstion. The solution was build in mind for 3 unique parameters.
