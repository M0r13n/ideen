The following constraints that are limiting the [[Value Stream]] are:

- **Environment Creation:** production and test environments should be created on demand and be fully self-serviced. By using principles like Infrastructure as Code ([[Ansible]]) environments can be created automatically, so that they are available when they are needed.
- **Code Deployment:** deployments should be automated as much as possible. Ideally, a complete deployment can be performed by the click of a button by a single engineer.
- **Test setup:** tests should be fully automated and parallelized so that each code change can be individually verified. It should not be necessary to spent days or weeks to create test environments. 