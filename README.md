# kafka-experiment
## To start running site monitoring app
- docker build -t myimage .
- docker run -e URL='http://google.com' -e PATTERN='.\*google.\*' -it myimage
