import json
import logging
import subprocess
from pathlib import Path

import munch
import pytest
from atomkraft.chain import Testnet
from atomkraft.chain.utils import TmEventSubscribe
from modelator.pytest.decorators import step

keypath = "action.tag"


@pytest.fixture
def home_dir(tmp_path):
    return tmp_path / "blogd-client"


@step("Nil")
def init(testnet: Testnet, home_dir: Path):
    logging.info("Step: Nil")
    testnet.set_accounts(["alice", "bob"])
    testnet.set_account_balances({"alice": int(1e10), "bob": int(1e10)})
    testnet.verbose = True
    testnet.oneshot()

    with TmEventSubscribe({"tm.event": "NewBlock"}):
        logging.info("\tTestnet is launched...")

    for (user, account) in testnet.accounts.items():
        args = (
            f"{testnet.binary} "
            f"keys add {user} "
            "--recover "
            "--keyring-backend test "
            f"--home {home_dir} "
        ).split()
        subprocess.run(
            args,
            check=True,
            input=f"{account.wallet.mnemonic()}\n".encode(),
        )


@step("Post")
def post(testnet: Testnet, home_dir: Path, action):
    logging.info("Step: Post")
    creator = action.value.creator
    title = action.value.title
    body = action.value.body

    rpc_addr = testnet.get_validator_port(0, "rpc")

    args = (
        f"{testnet.binary} "
        "tx blog "
        f"create-post title-{title} body-{body} "
        f"--from {creator} "
        "--broadcast-mode block "
        "-y "
        "--keyring-backend test "
        f"--home {home_dir} "
        f"--chain-id {testnet.chain_id} "
        f"--node {rpc_addr} "
        "--output json "
    ).split()
    proc = subprocess.run(args, check=True, capture_output=True)

    result = None
    if proc.stdout:
        result = json.loads(proc.stdout.decode())

    if result is None:
        logging.info("\tNo response!!")
    elif result["code"] == 0:
        logging.info("\tSuccessful!")
    else:
        code = result["code"]
        msg = result["raw_log"]
        logging.info(f"\tFailure: (Code {code}) {msg}")

    if proc.stderr:
        logging.info(f"\tstderr: {proc.stderr.decode()}")


@step("Query")
def query(testnet: Testnet, home_dir: Path, action):
    logging.info("Step: Query")
    blogs = munch.unmunchify(action.value)

    rpc_addr = testnet.get_validator_port(0, "rpc")

    args = (
        f"{testnet.binary} "
        "q blog "
        "posts "
        f"--home {home_dir} "
        f"--chain-id {testnet.chain_id} "
        f"--node {rpc_addr} "
        " --output json "
    ).split()
    proc = subprocess.run(args, check=True, capture_output=True)

    data = None
    if proc.stdout:
        data = json.loads(proc.stdout.decode())["Post"]

    logging.info("\tBlog list:")
    logging.info(f"\t\tExpected: {blogs}")
    logging.info(f"\t\tObserved: {data}")

    if proc.stderr:
        logging.info(f"\tstderr: {proc.stderr.decode()}")
