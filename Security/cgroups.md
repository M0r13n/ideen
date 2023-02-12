- Control Groups
- allocate system resources:
	- CPU time
	- memory
	- network bandwidth
- groups of **tasks** (processes)
- hierarchical structure:
	- a **hierarchie** is a (hierarchical tree of cgroups)
	- child groups inherit attributes from their parents
	- there are many different hierarchical trees unlike the single process tree (with `init` as its root)
- a **subsystem** represents a single resource
	- cpu
	- memory
	- network
	- ...

## Basic Rules

- <mark>a single hierarchy can have one or more subsystems attached to it </mark>
	- e.g. `cpu_mem_cg` with `cg1` and `cg2` as its children
-  <mark>a subsystem  cannot be attached to more than one hierarchy</mark>
	- e.g. if there is `cpu_mem_cg` the CPU and Memory subsystems can not be attached to another hierarchie
-  <mark>tasks on the system are initially members of the default cgroup of each hierarchy</mark>
-  <mark>child tasks (processes) inherit the cgroup membership of its parents but can be moved to different cgroups as needed</mark>

## Consequences

- task can belong to only a single cgroup in any one hierarchy
- you can group several subsystems together so that they affect all tasks in a single hierarchy
