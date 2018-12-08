# App Dependencies Docker File

This image is responsible for pulling in the app dependencies needed to run the Python project. It inerits from `../build-dependencies` and needs to have a `requirements.txt` file add in. In GR History's case, there are multiple files referenced in the `wagtail-cookiecutter` project, so that needs to be kept in mind.

Because we need to include project files in this image, the build command isn't as straight-forward as the build depencies image. The Dockerfile expects the files to be in the context root, but this file exists outside of that file structure. Thankfully Docker has arguments to compensate for that. From the project root run: `docker build -t grhistory/app_deps:latest -f ./devops/dockerfiles/app-dependencies/Dockerfile ./app/src`. Just like the build dependencies, the tag isn't too important in and of itself. But our final app-runner image will inherit from this image, so that will need to be kept in sync.

This file will need to be changed and the image rebuilt if the app dependencies change. Dependencies changes might also require a change and rebuilt of the built dependencies image.
