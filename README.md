# Project Health Cli

Read-only JavaScript project readiness checks for scripts, lockfiles, documentation and repository layout.

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) ![License MIT](https://img.shields.io/badge/License-MIT-green)

## Quick start

Python 3.10+; standard library only. Clone or extract the repository, then run from its root.

```bash
python3 health.py /path/to/project --strict
```

## Scope and limitations

Heuristic root-package checklist, not a build/test runner, vulnerability scanner or quality score. A project with no test/build script may be valid; review findings. For monorepos, inspect the relevant package separately. Exit 1 on errors or, in strict mode, warnings.



## Development

```bash
python3 -m unittest discover -s tests -v
```



## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Please do not publish real credentials, customer data or sensitive reports in issues.

## License

MIT — see [LICENSE](LICENSE).
