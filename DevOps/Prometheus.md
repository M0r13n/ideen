# Prometheus

Prometheus is an Open-Source Monitoring and Altering system, that was developed by SoundCloud in 2012. Since 2016 it is part of the *Cloud Native Computing Foundation*, like Kubernetes. 


## Architecture

Prometheus uses a <mark>pull model</mark> to collect metrics:
A Prometheus server periodically scrapes HTTP endpoints that expose metrics.
These endpoints can either natively expose their own metrics or through any of the thousands of third party exporters.
These exporters are used to allow Prometheus to collect metrics from every system.
There is also the possibility to push metrics to Prometheus using the so called Agent mode.
This can be useful when the targets are in a different subnet that is firewalled.

<mark>The metrics are exposed via HTTP in a simple text format (ASCII).</mark>
This is light weight, portable and human readable.

## Metrics
There are **four** different metrics available in Prometheus:

- **Counter**: Simple counter that can only be **incremented**. Can be **reset to zero**. Typical examples for counters are **error counts** or **page views**.
- **Gauge**: Variable values that fluctuate. Values are constantly increasing or decreasing. Typically seen when monitoring CPU usage, RAM usage or JVM heap size. 
- **Histogram**: Summarizes statistical information. E.g. response time
- **Summary**: Summary metrics are used to track the size of events, usually how long they take. Typically it consists of two counters + some gauges. 

Fundamentally, every metric is a data point made of:

- a name (e.g. `system_cpu_time`)
- a timestamp when is was collected
- a numeric value -> the measurement

### Labels

Additionally, each metric can have a set of labels.
<mark>Labels are simple key-value pairs used to uniquely identify metrics.</mark>
Any given combination of labels for the same metric name identifies a particular dimensional instantiation of that metric.
So `current_humidity{room="bathroom"}` and `current_humidity{room="living_room"}` share the same metric name, but can be used as two distinct metrics for two different rooms.

This is an example of a single metric:

```txt
# HELP current_humidity the current humidity percentage
# TYPE current_humidity gauge
current_humidity{room="bathroom"} 64.7
```

The keyword `# HELP` provides some kind of description about the metric.
`# TYPE` defines the type of the metric, which can be any of the four basic types listed above.


### Naming conventions

Metrics should be named after the following pattern:

`<PREFIX>_<NAME><SUFFIX>`

where,

- **PREFIX**:
  - is a namespace for the given metric
  - it is used to give the metric some context
  - e.g. application name (mktxp) or service name (http)
- **NAME**: 
  - is a name for the metric
  - tells us, what is measured
  - e.g. cpu_seconds, humidity, request_duration
- **SUFFIX**: 
  - is used to describe the unit
  - seconds, bytes, total, info
  - [Base Units](https://prometheus.io/docs/practices/naming/#base-units)

### Metadata

So, if Prometheus only allows to store numeric metrics, how can I store meta data. It could be handy so store the software version, branch or commit. 

To achieve this a single time series is exposed that always has the value 1.
The information is then stored as labels.

```python
build_info = Gauge('prometheus_build_info', 'Build information', 
    ['branch', 'goversion', 'revision', 'version'])
build_info.labels('HEAD', 'go1.6.2', 
    '16d70a8b6bd90f0ff793813405e84d5724a9ba65', '1.0.1').set(1)
```

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

###  Retention Period

- defaults to 15 days
- any time series data older than that is deleted
- can be customized by adding to following parameter when calling Prometheus:
	- `--storage.tsdb.retention.time=1y"`

## Terms

### Time Series

- series of **(timestamp, value)** tuples
- sorted by timestamp
- timestamps use millisecond precision
- each time series is **uniquely identified** by its name and a set of labels:
	- `temperature`
	- `temperature{city=”NY”}`
	- `temperature{city=”SF”}`
	- `temperature{city=”SF”, unit=”Celsius”}`
	- `humidity`

### Data Point

- a single **(timestamp, value)** tuple is called a **data point**

### Cardinality

- number of unique time series stored in Prometheus
- defined by the sum of all distinct time series:
	- count of distinctt values for one label
	- the number of labels
	- the number of distinct metric names
		- `temperature`
		- `temperature{city=”NY”}`
		- `temperature{city=”SF”, unit=”Fahrenheit”}`
		- `temperature{city=”SF”, unit=”Celsius”}`
		- `C = 2 x 2 = 4`
			- two different labels (city, unit) with two different values each (NY/SF and Fahrenheit/Celsius)

### Ingestion Rate

- per second number of data points inserted into Prometheus
- depends on:
	- total number of scraped targets
	- scrape interval
	- `ingestion_rate = num_targets * metrics_per_target / scrape_interval`