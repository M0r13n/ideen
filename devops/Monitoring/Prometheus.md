# Prometheus

Prometheus is an Open-Source Monitoring and Altering system, that was developed by SoundCloud in 2012. Since 2016 it is part of the *Cloud Native Computing Foundation*, like Kubernetes. 


## Architecture


## Metrics
There are **four** different metrics available in Prometheus:

- **Counter**: Simple counter that can only be **incremented**. Can be **reset to zero**. Typical examples for counters are **error counts** or **page views**.
- **Gauge**: Variable values that fluctuate. Values are constantly increasing or decreasing. Typically seen when monitoring CPU usage, RAM usage or JVM heap size. 
- **Histogram**: Summarizes statistical information. E.g. response time
- **Summary**: Summary metrics are used to track the size of events, usually how long they take. Typically it consists of two counters + some gauges. 

## PromQL
Query language used by Prometheus. It is read only.

### Examples

Select all time series metrics that have the `mikrotik_system_cpu_load` metric name:

`mikrotik_system_cpu_load`

These time series can be filtered by appending comma separated matchers (key-value pairs) to the query (Note that there is no space between the values):

`mikrotik_system_cpu_load{address="192.168.0.1"}`
or 
`mikrotik_system_cpu_load{address="192.168.0.1",running="true"}`

Optional logical operators:
- `=`: equal
- `!=`: not equal
- `=~`: regex match
- `!~`: regex exclude

Get all DHCP leases for devices in the `192.168.0.0/16` network:

`mikrotik_dhcp_leases_metrics{address=~"192.168.*"}`

### Functions and operators

