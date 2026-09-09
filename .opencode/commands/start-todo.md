---
description: Start a backlog.md item on a new feature branch
---
Start backlog item section $1 number $2$3 (if $3 is present it replaces the derived slug).

Working tree must be clean first. Current status:
!`git status --short`

Steps:
1. If the status output above is non-empty, stop and report the dirty files. Never stash or discard without being asked.
2. Read @backlog.md, find section $1 item $2, and quote its title back.
3. Run `git checkout main && git pull`.
4. Derive the branch name as `<section>/<slug>`, where slug is the item title lowercased with non-alphanumeric runs replaced by single hyphens (for example section `infra` item `Swap to custom domain name` becomes `infra/swap-to-custom-domain-name`). If extra arguments were given after the number, join them with hyphens and use that as the slug instead.
5. If that branch already exists locally or on origin, check it out instead of creating it.
6. Otherwise create it with `git checkout -b <branch>` and confirm: item title, branch name, and that the next step is implementing the item plus opening a PR.
