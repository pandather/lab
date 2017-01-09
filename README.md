# Lab

API that tracks the status of UTCS GDC lab machines. Primarily, it provides suggestions on which lab machines to connect to based on its work status, uptime, users, and load.

## API Reference

### `/all`
Returns all UNIX hosts.

### `/up`
Returns UNIX hosts with an "up" status.

### `/down`
Returns UNIX hosts with a "down" status.

### `/users`
Returns UNIX hosts with users above or below the specified threshold. Parameters: up (boolean), threshold (int).

### `/load`
Returns UNIX hosts with load above or below the specified threshold. Parameters: up (boolean), threshold (float).

### `/uptime`
Returns UNIX hosts with an uptime above or below the specified threshold. Parameters: up (boolean), threshold (int).

### `/host`
Returns the specified UNIX host and its information. Parameters: name (String).

### `/sorted`
Returns a sorted list of UNIX hosts based on the lowest uptime, users, and load.
