# WebSocket API

## Format

Every message must be JSON and contain key `command` with string type.

Any data for this command will be a JSON object inside key `data`.

## Responses

Good responses look like:
```
{
  "status": "OK",
  "command": "ping",
  "data": { "pong": True }
}
```

Bad responses may have statuses:

- `MALFORMED` - The message sent in doesn't decode to valid JSON in the required format.
- `INVALID_COMMAND` - The command requested doesn't exist
- `INVALID_DATA` - The command exists, but the data parameters were invalid. This may have a data element `reason`.
- `SERVER_ERROR` - The server failed for some reason, `reason` may be returned.

`command` may be returned (if `command` was given).
`data` may be returned with response data if the command provides it.

## Commands

### ping

#### Returns

`{ "pong": True }`

#### Example
```
{
  "status": "OK",
  "command": "ping",
  "data": { "pong": True }
}
```

### demo_start

Starts a demo / display enumeration on connected display monitors.

#### Data Params

`monitor_indexes: []` - A list of integer monitor indexes to display the demo on. If empty, runs on all monitors.


