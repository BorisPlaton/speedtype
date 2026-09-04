# Speedtype
TUI for training typing speed.

## Table of Contents
- [What is Speedtype?](#what-is-speedtype)
- [Install & Update](#install--update)
- [Development](#development)
  - [Prerequisites](#prerequisites)
  - [Initialize the project](#initialize-the-project)
  - [Development conventions](#development-conventions)
    - [Developing](#developing)
    - [Pull requests](#pull-requests)

## What is Speedtype?

<img align="right" width="60%" src="https://github.com/user-attachments/assets/97ff5690-00ba-443b-beee-0bee1002abfb">
Configure your text training with various settings: language, time, words length, etc.

<br clear="both">
<br>

<img align="right" width="60%" hspace="" src="https://github.com/user-attachments/assets/26fcec08-dba8-4fa6-be3d-c57d5165bcbe">
Practice your typing with a selected configuration within a specific time range.

<br clear="both">
<br>

<img align="right" width="60%" src="https://github.com/user-attachments/assets/89ebf3f7-8238-40e0-8390-3eaa7a1c654f">
Review the mistakes made, your statistics, and your speed across the typing session.

<br clear="both">
<br>

## Install & Update

Install `speedtype` with:
```
curl -fsSL https://raw.githubusercontent.com/BorisPlaton/speedtype/refs/heads/main/speedtype/install.sh | sh
```

After installation, run:
```
speedtype
```

To update `speedtype`, run the same command as for installation.

## Development
This section is intended only for developing the *Speedtype*. If you only want to install the application, go to the [Setup](#Setup) section.

### Prerequisites

- [`uv`](https://docs.astral.sh/uv/) installed
- [`just`](https://github.com/casey/just) installed

### Initialize the project
1. Clone the repository
2. Run `just init`

### Development conventions

#### Developing
1. Checkout from the `main` a new branch with the following name `<feature/bugfix/task>/<short description>`.
   1. How to choose what to specify: *feature*, *bugfix* or *task*:
      - *feature* - adds a new functionality to the end users - it is what they will see when *Speedtype* is launched.
      - *bugfix* - fixing the bug that occurs in the *Speedtype*.
      - *task* - anything else: updating *README*, adding new tests, configuring linters, etc.
2. Do some changes...
3. Push the branch to the `origin`.
4. Create PR.

#### Pull requests
- Title must follow the next structure `<feature/bugfix/task>: <short description>`.
- PR's body must contain the following sections.
  - *What was done* - description of what was changed/added/removed.
  - *Issues* - link to the issue which will be resolved after PR is merged.
  - *Attachments* (optional) - contains the additional attachments: photo, videos, etc.
- Add appropriate labels.
- Apply only the ***squash and merge*** strategy when merging changes into the `main` branch.
  - Add PR description into the merge request's `Extended description`.
- After the PR is merged, delete the original branch.
