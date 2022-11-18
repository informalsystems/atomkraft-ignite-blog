# minimal archlinux image; not even base-devel
FROM archlinux

# dependencies
RUN pacman -Syu --needed --noconfirm gcc go python-pip git which java-runtime

# install ignite
RUN curl https://get.ignite.com/cli! | bash


# clone including ignite-blog submodule; and change directory
RUN git clone --recurse-submodules https://github.com/informalsystems/atomkraft-ignite-blog
WORKDIR /atomkraft-ignite-blog

# install atomkraft
RUN pip install -U atomkraft

# build blockchain binary
RUN (cd ignite-blog; ignite chain build --output dist)

# set up apalache
RUN atomkraft model apalache get

# generate traces
RUN atomkraft model check --model-path models/blog.tla --max_error=5 --view=View --invariants NotMixedPostQuery --traces-dir traces

# run atomkraft with a trace
RUN atomkraft test trace --path traces/NotMixedPostQuery/violation1.itf.json --reactor reactors/reactor.py --keypath action.tag
