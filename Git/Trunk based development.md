## Trunk-based development

- version control management practice where developers ==merge small, frequent updates to a core “trunk” or main branch==
- single branch called the “trunk” where developers directly commit
- release branches are read-only branches
- commit small changes often
- each  commit is a small part of the code, e.g. one function or method with unit tests
- when the trunk branch contains every feature that we want, one person creates a new release branch from the trunk.

- some real-world benefits include:
- users work at the “head,” or most recent, version of a single copy of the code
- changes are made to the repository in a single, serial ordering
- single consistent view of the codebase
- no pain-ful merges that often occur when it is time to reconcile long-lived branches