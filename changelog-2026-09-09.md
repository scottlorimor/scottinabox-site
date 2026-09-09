# changelog — 2026-09-09

### Model switch to Muse Spark 1.3
- Switched opencode config to Muse Spark 1.3 via OpenRouter

### Listing available LSPs
- Reported opencode built-in LSP table backed by docs plus local status

### Add Hugo test suite plus CI
- Added tests/test_site.py (python3 stdlib, 4 checks: build, pages, links, stale refs)
- Wired CI test job into .github/workflows/hugo.yaml
- Opened PR #2 from infra/test-suite (merged)

### Push updates, ensure PR, sync todos
- Verified infra/test-suite pushed clean, confirmed PR #2 open
- Confirmed backlog test-suite item marked done

### Start-todo subagent plus PR #3 merge
- Added .opencode/agents/start-todo.md (subagent, git-only bash, edits denied)
- Set start-todo command to agent start-todo plus subtask true
- Committed, pushed, merged PR #3 to main
- Verified site checks green on main

### Custom domain scottlorimor.com plus PR #4
- Set hugo.toml baseURL to https://scottlorimor.com/
- Added static/CNAME with scottlorimor.com
- Updated tests/test_site.py (prefix from hugo.toml, CNAME expected, github.io stale pattern)
- Updated README, tech-stack.md, CLAUDE.md, marked backlog infra 2 done
- Verified all checks green plus subpath regression probe
- Opened PR #4, merge blocked on DNS plus Pages custom-domain setup

---

**Token totals:** 724.9k in | 48.9k out | 32.1k reasoning | 16934.0k cache read | 0.0k cache write | $0.06
