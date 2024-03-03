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

## Administration

- Postgresql version: `sudo gitlab-psql --version`

## Mint a PAT via SSH

` ssh git@gitlab.com personal_access_token someTokenName api,read_repository,read_api,read_user,read_registry 90`

## Delete uploaded files

Send a GraphQL query:

```graphql
mutation{
  uploadDelete(input: { projectPath: "YOUR_PROJECT_PATH", secret: "YOUR_SECRET_HASH_KEY" , filename: "FILE_NAME" }) { 
    upload {
      id
      size
      path 
    }
    errors
  }
}
```

- https://stackoverflow.com/questions/65087695/how-can-i-completely-delete-a-file-that-was-uploaded-to-gitlab-in-an-issue-comme
- https://gitlab.com/gitlab-org/gitlab/-/merge_requests/92791
