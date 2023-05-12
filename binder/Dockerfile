FROM yxzhan/intel4coro:binderhub-0.0.7

WORKDIR /home/${NB_USER}/

# RUN pip install jupyterlab-cell-flash jupyterlab-search-replace stickyland
RUN git clone https://github.com/IntEL4CoRo/ease_fall_school_2022.git -b binderhub
RUN jupyter lab workspaces import /home/${NB_USER}/ease_fall_school_2022/binder/workspace.json

WORKDIR /home/${NB_USER}/ease_fall_school_2022/
