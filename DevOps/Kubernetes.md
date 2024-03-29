# Kubernetes

- **Container:** Containers are the units of packaging used to bundle application binaries together with their dependencies, configuration, framework, and libraries.
- **Pods:** Pods are the deployment units in Kubernetes ecosystem which contains one or more containers together on the same node. Group of containers can work together and share the resources to achieve the same goal.
- **Node:** A node is the representation of a single machine in the cluster running Kubernetes applications. A node can be a physical, bare metal machine or a virtual machine.
- **Cluster:** Several Nodes are connected to each other to form a cluster to pool resources that are shared by the applications deployed onto the cluster.
- **Persistent Volume:** Since the containers can join and leave the computing environment dynamically, local data storage can be volatile. Persistent volumes help store container data more permanently.

## My Take

I see K8s primarily as a development tool, enabling quick setup and portability for developers but find it lacking for production due to operational challenges.
