# rye-pre-commit

A cross-platform [pre-commit](https://pre-commit.com/) hook for [rye](https://github.com/astral-sh/rye). The hook uses the system's `rye`.

## Using Rye with pre-commit

To run `rye test` and `rye lock` via pre-commit, add the following to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/itsjohncs/rye-pre-commit
  rev: v0.1.0
  hooks:
  - id: rye-test
  - id: rye-lock
```

To run an abitrary `rye` command, you can use the `rye` or `rye-with-filenames` hooks (the latter is given the list of changed files).

```yaml
- repo: https://github.com/itsjohncs/rye-pre-commit
  rev: v0.1.0
  hooks:
  - id: rye
    args: ["sync"]
  - id: rye-with-filenames
    args: ["run", "black"]
```
