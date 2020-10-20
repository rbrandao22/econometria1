docker run -it --rm --net host --name python-interactive -v "$PWD":/usr/src/app --entrypoint bash my-python-app
