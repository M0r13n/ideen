# Tips and Tricks for apt

- install apt non interactively: `DEBIAN_FRONTEND=noninteractive apt-get -y`
- search for packages: `apt search firefox`
- inspect package `apt show firefox`
- clean up: `apt clean`

## Prevent installation of package(s)

- edit **/etc/apt/preferences**

  ```txt
  Package: <nameofpackage_1> <nameofpackage_...> <nameofpackage_N>
  Pin: release *
  Pin-Priority: -1
  ```

- `Pin: origin ""` does not work on recent versions of Ubuntu (22.04+)

- `Package:` takes any number $\N_{\ge1}$ of package names

- even patterns are possible: `firefox-*`

