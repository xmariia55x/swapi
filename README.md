# Star Wars API

## Run the project on Windows/Mac/Linux

I assume you already have Docker installed in your machine.
Before executing the container make sure that you don't have any process running on your local port 5000. 

```
cd app
docker build -t star-wars-api .
docker run -p 5000:5000 star-wars-api
```

Open Postman or use curl to start making requests to the API. 

There is an endpoint called `/people/data` which returns the information from the people endpoint that the Star Wars API offers sorted in ascending order. 
To call it, make this request:

```
GET http://localhost:5000/people/data?all=true
```

It will return a list containing all the people. You could also pass in the request parameters the following one: `page=2` and it will return the people that are in the second page. 
The API returns paginated results so that is why I added the possibility of requesting only one page results. The request will look like:

```
GET http://localhost:5000/people/data?page=2
```

In case you do not specify any request params, it will return the results from the first page. The request will be: 

```
GET http://localhost:5000/people/data
```

## Deploy the application in minikube using Helm Charts

I assume you already have minikube and Helm installed. Also, I assume you already have your minikube up and running. 

From the root directory of the project run this command: 

```
helm install star-wars-api ./helm-chart
```

And this will create the necessary Kubernetes resources to start the application. 

You can execute `kubectl get pods` to verify that a pod was created and create a port-forward to start making requests to the API with this command `kubectl port-forward pod/<pod-name> 5000:5000` 

To remove the Kubernetes resources you only need to run `helm uninstall star-wars-api` and it will remove the chart from the Kubernetes cluster. 

## CI/CD workflow

In order to ensure that the continous delivery and deployment of the application is made according to the best practices, a workflow has been created to ensure that the code complies with the best standards. 

This workflow is in charge of running the tests, linting the code using MegaLinter a powerful set of linters with minimal configuration, logging into the GitHub Container Registry that is where the docker container will be stored and then building and pushing the Docker image to the registry. It also runs performance tests using K6. 

## Performance tests

### How to run them

When you make a push to the main branch of this repository, you will see that a new action is triggered. In that action the performance tests are executed using K6's GitHub action. In case you want to run the performance tests in your computer, make sure to have K6 installed using the instructions provided in [this page](https://grafana.com/docs/k6/latest/set-up/install-k6/). 

To execute the tests, you just need to run this command `k6 run load-tests/star-wars-api-test.js` from the root directory of the project.

### How to interpret the results

In this case I have defined a metric that tests the successful requests: ['rate>0.95']. This metric requires at least 95% of the requests to be successful during a load test.

Interpretation:
- If more than 95% of requests succeed, the system handles the load.
- If less than 95%, the system fails to manage the load and needs optimization.