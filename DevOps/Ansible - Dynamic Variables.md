The following is an example on how to get dynamic variables based in the hostname. This can be used to define different values for the same variables for each host in a single file. This may be much more maintainable depending on the use case.

```yml
clients:
  hostname1:
    id: id_1
    value: value_1
  hostname2:
    id: id_2
    value: value_2
```

Then in your template:

```Jinja2
{{ clients[inventory_hostname].id }}
```