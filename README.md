# atomkraft-ignite-blog

## Atomkraft on Ignite tutorial

1. Follow the [Ignite blog tutorial](https://docs.ignite.com/guide/blog) and setup `blogd` at the system path via `ignite chain build`.
2. Install atomkraft `pip install -U atomkraft`.
3. Invoke an Atomkraft test, `atomkraft test trace --path traces/violation5.itf.json --reactor reactors/reactor.py --keypath action.tag`.

## Directory structure

|    Path    | Description                                    |
| :--------: | ---------------------------------------------- |
|  `models`  | Contains a specification for Blog API.         |
|  `traces`  | Generated traces from the specification.       |
| `reactors` | Methods to map traces to real test executions. |
