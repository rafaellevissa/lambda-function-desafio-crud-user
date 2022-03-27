# Hitbel

### Usage

The endpoints can be found in the `hitbel.postman_collection.json` file.

### Deployment

To deploy the application to aws just need to run the folowing command.

```
$ serverless deploy
```

After run it, you should be able to see the endpoints and access them.

### Local development

You can run locally with the plugin serverless offline as shown below.

```
serverless offline
```

### Tests

Before you run the tests make sure you have all the dev_requirements installed on your machine. The requirements can be find in the root directory of the projetct `dev_requirements.txt`

```
pytest
```
