# GitLab Basics


## Organization
There are three different options to organize a given organization on GitLab. 

### Groups
- used for strategic planning, governance and management
- used to manage business initiatives and strategic planning
- allows to manage
	* sub groups
	* epics
	* milestones
	* roadmaps
	* labels
	* boards
	* projects
- groups are like folders
	- Each group can have nested groups (sub folders)
	- Inside each group there are $\mathbb{N}_{\ge0}$ projects (files)

### Subgroups
- nested, child groups for additional levels of organization
- otherwise they are just normal groups

### Projects
- where the *real work* is done
- this is where the team collaborates, plans work, writes code and delivers working apps
- based on a **single** repo
- allows to manage:
	- a single Repo
	- Issues & Discussion
	- Labels
	- Boards
	- Milestones
	- CI/CD Pipelines
	- Review Apps
	- Automatic deployments