## Atomkraft on Ignite-CLI blog tutorial

1. Clone the repository

```
git clone https://github.com/informalsystems/atomkraft-ignite-blog
cd atomkraft-ignite-blog
```

2. Pull `ignite-blog` git submodule. It is a ready-made example blockchain repo, following [Ignite-CLI tutorial](https://docs.ignite.com/guide/blog).

```
git submodule update --init --recursive
```

3. Build `blogd` from the example blockchain.

```
(cd ignite-blog; ignite chain build --output dist)
```

4. Install Atomkraft.

```
pip install -U atomkraft
```

If you need help, you can follow the [main installation guide](https://github.com/informalsystems/atomkraft/blob/dev/INSTALLATION.md).

5. Invoke an Atomkraft test.

```
atomkraft test trace --path traces/violation5.itf.json --reactor reactors/reactor.py --keypath action.tag
```

## Directory structure

|    Path    | Description                                    |
| :--------: | ---------------------------------------------- |
|  `models`  | Contains a specification for Blog API.         |
|  `traces`  | Generated traces from the specification.       |
| `reactors` | Methods to map traces to real test executions. |
