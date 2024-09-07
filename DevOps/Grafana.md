# $\_\_rate_interval variable

- based on the scrape interval of the Prometheus data source
- guaranteed to be at least four times the scrape interval
- can be used for most `rate()` queries

# Dashboard JSON

> grafana Failed to upgrade legacy queries Datasource ${DS_PROMETHEUS} was not found

This error means that Grafana failed to resolve the variable `${DS_PROMETHEUS}` during provisioning. This typically occurs when using dashboard exports from the share button. Instead, use the view json feature from dashboard settings view to get the dashboard json ([source](https://github.com/grafana/grafana/issues/11018#issuecomment-368472235)).
