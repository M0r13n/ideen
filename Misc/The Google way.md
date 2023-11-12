# What does Google differently to _normal_ companies?



On a technical level, Google:

- .. provides access to a gigantic monorepo with billions of lines of code ([source](https://dl.acm.org/doi/pdf/10.1145/2854146))
- .. ensures that only one version of an open source project be available at
  any given time for the whole codebase, by adding a dedicated section in their monorepo for open source libs

For its developers, Google:

- .. offers kind of a second passport. It offers an office with internet, food, desks and so forth in every major city across the globe ([source](https://shreyans.org/google))
- .. provides mentoring and access from/to legends from the industry

## Details

### Monorepo

- Google is the living proof that a gigantic monolithic model for source code can work (_can work, does not mean has to work!_)
- unifies versioning
- simplifies dependency management
- enables atomic changes
- extensive code sharing and reuse;
- most likely not feasible with any existing SCM including git
- Google uses its own SCM: **Piper**
  - provided file-based access control lists
  - visibility of files can be configured per user
  - **Clients in the Cloud**
    - local workspace behaves like a directory
    - allows to browse the whole repository
    - only modified files are stored locally
    - very efficient for large repos