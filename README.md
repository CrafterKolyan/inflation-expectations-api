# Inflation Expectations Estimation

Authors: Maksim Eremeev (mae9785@nyu.edu), Timothy Petlyar (tdp259@nyu.edu), Binur Zhalenov (bz1090@nyu.edu)

**Description**: This library features the API for the inflations expectation toolbox. Everything is operated by Docker. This is a pre-release, so it may contain bugs.

## Quick start

```bash
docker pull rabbitmq

docker run -it -d \
           --name rabbitmq \
	         -p 15672:15672 \
	         -p 5672:5672 \
	         -e RABBITMQ_DEFAULT_USER=guest \
 	         -e RABBITMQ_DEFAULT_PASS=guest \
	         rabbitmq:3-management

docker-compose build
docker-compose up
```

This builds and executes the **async HTTP server**, **RabbitMQ**, **Topic Modelling-based inference worker**. 

Then you easily make a POST request to the `localhost:22556/api/v1/run` containing a JSON with all document metadata. Check the `config.json` file to make sure all settings are correct.

## Codestyle check

Before making a commmit / pull-request, please check the coding style by running the bash script in the `codestyle` directory. Make sure that your folder is included in `codestyle/pycodestyle_files.txt` list.

Your changes will not be approved if the script indicates any incongruities (this does not apply to 3rd-party code). 

Usage:

```bash
cd codestyle
sh check_code_style.sh
```

