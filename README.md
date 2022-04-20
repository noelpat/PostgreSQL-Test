# PostgreSQL-Test

This is meant to run inside a docker container that will be able to access another container running a PostgreSQL database using environment variables.

Assuming the container is running and able to connect to the database, an example curl request to get "all" would be as follows:

curl --header "Content-Type: application/json" --request POST '172.17.0.3:8080/'

To get one book or a selection, you can pass the work IDs in a list like so:

curl --header "Content-Type: application/json" --request POST --data '{"value":[1,2]}' '172.17.0.3:8080/selection'
