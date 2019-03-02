# Galaxy - GraphClust
FROM quay.io/bgruening/galaxy:19.01

MAINTAINER Björn A. Grüning, bjoern.gruening@gmail.com

ENV GALAXY_CONFIG_BRAND GraphClust
ENV ENABLE_TTS_INSTALL True

# Install tools
# Split into multiple layers, it seems that there is a max-layer size.
COPY ./assets/tools/graphclust_tools.yml $GALAXY_ROOT/tools.yaml
RUN install-tools $GALAXY_ROOT/tools.yaml && \
    /tool_deps/_conda/bin/conda clean --tarballs --yes && \
    rm /export/galaxy-central/ -rf

COPY ./assets/tools/graphclust_tools2.yml $GALAXY_ROOT/tools_2.yaml
RUN install-tools $GALAXY_ROOT/tools_2.yaml && \
    /tool_deps/_conda/bin/conda clean --tarballs --yes && \
    rm /export/galaxy-central/ -rf 

COPY ./assets/tools/graphclust_utils.yml $GALAXY_ROOT/tools_3.yaml
RUN install-tools $GALAXY_ROOT/tools_3.yaml && \
    /tool_deps/_conda/bin/conda clean --tarballs --yes && \  
    rm /export/galaxy-central/ -rf 


# Add Galaxy interactive tours
ADD ./assets/tours/* $GALAXY_ROOT/config/plugins/tours/

# Data libraries
ADD ./assets/library/library_data.yaml $GALAXY_ROOT/library_data.yaml

# Add workflows to the Docker image
ADD ./workflows/*.ga $GALAXY_ROOT/workflows/

# Download training data and populate the data library
RUN startup_lite && \
    sleep 30 && \
    . $GALAXY_VIRTUAL_ENV/bin/activate && \
    workflow-install --workflow_path $GALAXY_ROOT/workflows/ -g http://localhost:8080 -u $GALAXY_DEFAULT_ADMIN_USER -p $GALAXY_DEFAULT_ADMIN_PASSWORD 
    # && \
    # setup-data-libraries -i $GALAXY_ROOT/library_data.yaml -g http://localhost:8080 -u $GALAXY_DEFAULT_ADMIN_USER -p $GALAXY_DEFAULT_ADMIN_PASSWORD

# Container Style
ADD ./assets/img/workflow_early.png $GALAXY_CONFIG_DIR/web/welcome_image.png
ADD ./assets/welcome.html $GALAXY_CONFIG_DIR/web/welcome.html
