# kafka-experiment
1-st Step:
docker build -t myimage .
2-nd Step:
docker run -e URL='http://google.com' -e PATTERN='.*google.*' -it myimage
