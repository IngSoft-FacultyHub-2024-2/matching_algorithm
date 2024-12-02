# matching_algorithm

# Desarrollar en docker

Requirements:
- Docker installed

Run it with:
```
docker compose watch
```
#### Open in another terminal a terminal of the container:

```
docker exec -it <container_name> ../bin/bash
```
Example:

```
docker exec -it matching_algorithm-app-1 ../bin/bash
```

Stop running it with:
```
docker compose down
```

### build docker:
```
docker build -t my-python-app .
```

### docker run:
```
docker run -it my-python-app
```

### save the versions of the libraries:
```
pip freeze > requirements.txt
```

### Run api
```
uvicorn src.app:app --reload
```