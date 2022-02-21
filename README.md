use dynamodump from virual machine, Oracle VM box:
- update the local IP for NAT in the VM
- run `ssh -p 2222 jan@10.0.2....IP`
or using docker. \
build: \
`docker build -f ./Dockerfile.ubu -t ubuntu-py .`

run interactively:  
`docker run --rm -it -v $(pwd):/code ubuntu-py`