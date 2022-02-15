# Mind Map API

A [mind map](https://en.wikipedia.org/wiki/Mind_map) web service.

## Deployment

1. Get Python 3
2. (Optional) Set the `FLASK_ENV` environment variable
3. Run the `./bin/run.sh` script from the root directory
```bash
./bin/run.sh
```

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
