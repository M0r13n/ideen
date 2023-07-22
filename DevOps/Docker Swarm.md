# Docker Swarm

- **Node:** A node is a machine that runs an instance of Docker Engine
- **Swarm:** A cluster of Docker Engine instances.
- **Manager Node:** Manager nodes distribute and schedule incoming tasks onto the Worker nodes and maintains the cluster state. Manager Nodes can also optionally run services for Worker nodes.
- **Worker Node:** Worker nodes are instances of Docker Engine responsible for running applications in containers.
- **Service:** A service is an image of a microservice, such as web or database servers.
- **Task:** A service scheduled to run on a Worker node.
- A [reasonable comparison to Kubernetes](https://www.suse.com/c/rancher_blog/kubernetes-vs-docker-swarm-comparison-of-two-container-orchestration-tools/)
- k3s can be a good [alternative](https://traefik.io/glossary/k3s-explained/)
- interesting discussion on [HN 2021](https://news.ycombinator.com/item?id=29448182)

## Setup (simplified)

1. Install Docker on each physical machine: Start by installing Docker on each physical machine you want to include in the Docker Swarm cluster. This can be done by following the official Docker installation instructions for your specific operating system.
2. Initialize the Swarm on one of the machines: Choose one of the physical machines to be the manager node and use the `docker swarm init` command to initialize the Swarm on that machine.
3. Join other machines to the Swarm: On each additional physical machine that you want to add to the Swarm, use the `docker swarm join` command with the appropriate token provided during the `docker swarm init` step.
4. Deploy services or containers: Once the Swarm is set up, you can use standard Docker commands, such as `docker service create`, to deploy and manage containers as services across the entire cluster.
5. Scale services: Docker Swarm allows you to easily scale services horizontally by specifying the number of replicas for a particular service.
6. Monitor the cluster: Docker Swarm provides built-in tools for monitoring the cluster's health and performance.