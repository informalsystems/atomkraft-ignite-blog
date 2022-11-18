## Atomkraft on Ignite-CLI blog tutorial

### Software dependencies

|                          Name                          |                    Why                     |
| :----------------------------------------------------: | :----------------------------------------: |
|                          Git                           |              clone git repos               |
|                           Go                           |                 ignite-cli                 |
|                          Gcc                           | build some of the Atomkraft's dependencies |
|                          Java                          | Apalache (model checker used in Atomkraft) |
| [Poetry](https://python-poetry.org/docs/#installation) |        python project and Atomkraft        |
|    [Ignite](https://docs.ignite.com/guide/install)     |                 ignite-cli                 |

> **Note**: Make sure all dependencies are at their latest version.

### Instructions

1. Clone the repository

```bash
git clone https://github.com/informalsystems/atomkraft-ignite-blog
cd atomkraft-ignite-blog
```

2. Pull `ignite-blog` git submodule. It is a ready-made example blockchain repo, following [Ignite-CLI tutorial](https://docs.ignite.com/guide/blog).

```bash
git submodule update --init --recursive
```

3. Build `blogd` from the example blockchain.

```bash
(cd ignite-blog; ignite chain build --output dist)
```

4. Initialize a Poetry environment and install Atomkraft in it.

```bash
poetry install --no-root
```

5. Activate poetry shell

There are two ways of doing it.

- Spawn a sub-shell.

```bash
poetry shell
```

> **Note**: When you're done, use `exit` command or <kbd>Ctrl</kbd>+<kbd>D</kbd> to exit the sub-shell.

- Update the current shell environment.

```bash
source $(poetry env info -p)/bin/activate
```

> **Note**: When you're done, use `deactivate` command to revert to the original environment configuration.

6. Set up Apalache model checker.

```bash
atomkraft model apalache get
```

6. Generate traces from the model.

```bash
atomkraft model check --model-path models/blog.tla --max_error=5 --view=View --invariants NotMixedPostQuery --traces-dir traces
```

7. Invoke an Atomkraft test.

To run a single test using a single trace.

```bash
atomkraft test trace --path traces/NotMixedPostQuery/violation1.itf.json --reactor reactors/reactor.py --keypath action.tag
```

Or run multiple tests using all traces in a directory.

```bash
atomkraft test trace --path traces --reactor reactors/reactor.py --keypath action.tag
```

## Directory structure

|    Path    | Description                                    |
| :--------: | ---------------------------------------------- |
|  `models`  | Contains a specification for Blog API.         |
|  `traces`  | Generated traces from the specification.       |
| `reactors` | Methods to map traces to real test executions. |
