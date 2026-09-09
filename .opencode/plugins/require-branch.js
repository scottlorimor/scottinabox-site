// Block file edits on main so every backlog item starts on a feature branch.
// See .opencode/commands/start-todo.md for the entry point.
//
// Scope: edit and write tools only. Reads, search, and shell stay allowed so
// inspection never breaks. Bash mutations are covered downstream by
// .githooks/pre-push and GitHub branch protection. Fail-open: non-git
// directories and git errors allow the edit.

export const RequireBranchPlugin = async ({ directory, $ }) => {
  async function currentBranch() {
    try {
      const result = await $`git branch --show-current`
        .cwd(directory)
        .quiet()
        .nothrow();
      return result.exitCode === 0 ? result.text().trim() : null;
    } catch {
      return null;
    }
  }

  return {
    "tool.execute.before": async (input) => {
      if (input.tool !== "edit" && input.tool !== "write") return;
      const branch = await currentBranch();
      if (branch === "main") {
        throw new Error(
          "Direct edits on main are blocked. " +
            "Run /start-todo <section> <n> to create a feature branch first."
        );
      }
    },
  };
};
