# Mind Map API

We want you to design a [mind map](https://en.wikipedia.org/wiki/Mind_map) web service.

Your service must provide REST API endpoints to create a mind map and store its data in a backend.

Your solution must be written in **Python**.

## Deployment

The provided `./bin/run.sh` script must be enough to build and / or start the REST API.

## Specifications

### Create a mind map

```bash
curl -X PUT localhost:3000/api/v1/maps -H 'content-type: application/json' -d '{"id": "my-map"}'
```

### Add a leaf (path) to the map

```bash
$ curl -X PUT localhost:3000/api/v1/maps/[mapId]/leaves \
  -H 'content-type: application/json' \
  -d '{
    "path": "i/like/potatoes",
    "text": "Because reasons"
}'
```

### Read a leaf (path) of the map

```bash
$ curl -X GET localhost:3000/api/v1/maps/[mapId]/leaves?path=[path] -H 'content-type: application/json'

Sample response:
{
    "path": "i/like/potatoes",
    "text": "Because reasons"
}
```

### Pretty print the whole tree of the mind map

```bash
$ curl -X GET localhost:3000/api/v1/tree/[mapId]

Sample output:
root/
    i/
        like/
            potatoes
        eat/
            tomatoes
```
