FROM gitpod/workspace-full

USER gitpod

RUN bash -cl "rustup install nightly && rustup default nightly"

RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sudo sh

RUN npm i -g prettier