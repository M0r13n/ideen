# $__rate_interval variable

- based on the scrape interval of the Prometheus data source
- guaranteed to be at least four times the scrape interval
- can be used for most `rate()` queries