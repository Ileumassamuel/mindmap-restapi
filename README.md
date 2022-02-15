# Mind Map API

A [mind map](https://en.wikipedia.org/wiki/Mind_map) web service.

## Specifications

### Create a mind map

```bash
$ curl -X PUT localhost:3000/api/v1/maps -H 'content-type: application/json' -d '{"id": "my-map"}'
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

## Running

1. Get Python 3 (Tested with Python 3.10.2)
2. (Optional) Set the `FLASK_ENV` environment variable
3. Run the `./bin/run.sh` script from the root directory
```bash
$ ./bin/run.sh
```


## Development

The first three steps are automagically done the first time you run the
`./bin/run.sh` script.

1. Create a venv
```bash
$ python -m venv venv
```

2. Install the packages in `requirements.txt`
```bash
$ pip install -r requirements.txt
```

3. Set the `FLASK_APP` environment variable
```bash
$ export FLASK_APP=index.py
```

4. PROFIT


## Testing

First, make sure the first three steps of the (Development)[development] section
have been followed.

To run all tests
```bash
$ flask test
```

To run a specific test
```bash
$ flask test tests.testLeafApi
```
