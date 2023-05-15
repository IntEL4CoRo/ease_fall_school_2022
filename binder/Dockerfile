FROM yxzhan/intel4coro:binderhub-0.0.7

WORKDIR /home/${NB_USER}/

# RUN pip install jupyterlab-cell-flash jupyterlab-search-replace stickyland
ARG REPO_URL
# ADD https://api.github.com/repos/IntEL4CoRo/ease_fall_school_2022/git/refs/heads/binderhub version.json
RUN git clone -b binderhub ${REPO_URL}.git

RUN jupyter lab workspaces import /home/${NB_USER}/ease_fall_school_2022/binder/workspace.json

WORKDIR /home/${NB_USER}/ease_fall_school_2022/

ENTRYPOINT ["/home/jovyan/ease_fall_school_2022/binder/init.sh"]
