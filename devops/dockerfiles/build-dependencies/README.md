# Build Dependencies Docker File

This image will be the base for all the Python-related setup of the app. It's purpose is to add all the additional packages needed to build the app (including app dependencies), and allow the dependencies to be deleted off the final image.

No host files are needed in the image. To build, just `cd` into this directory and run `docker build -t grhistory/build_deps:latest .`. The image tag is just a suggestions, and other version codes other than `latest` may be necessary in the future. Just remember that the tag will be used to reference this image as a base in the `../app-depedencies` Dockerfile.

The file should only need to be changed if new app depencies require different libraries to compile, or dependencies are removed and certain packages are no longer required.
