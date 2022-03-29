# Project Generation Tool : git-cct
Github Create Clone Tool : git-cct
This generates projects, creates a repository for development team to work on.

### Installing Dependencies

- Copy environments and change the required configurations.
  `cp sample.env .env`
- Install requirements.
  `pip3 install -r requirements.txt`
- Verify installed requirements.
  `pip3 freeze | grep package_name`

### Running Script

After dependencies installation is completed.

```sh
python3 project_creation.py project_template project_name –out-path path_to_store_project
```

| Options            | Description                                               |
| ------------------ | --------------------------------------------------------- |
| `project_template` | one of `mobile`, `backend` or `frontend`                  |
| `project_name`     | Name of the project as per requirement                    |
| `out-path`         | Define the path where you would like to clone the project |