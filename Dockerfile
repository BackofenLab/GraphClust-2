# Galaxy - GraphClust

FROM bgruening/galaxy-stable:16.10

MAINTAINER Björn A. Grüning, bjoern.gruening@gmail.com

ENV GALAXY_CONFIG_BRAND GraphClust
ENV ENABLE_TTS_INSTALL True

# Enable Conda dependency resolution
ENV GALAXY_CONFIG_CONDA_AUTO_INSTALL=True \
    GALAXY_CONFIG_CONDA_AUTO_INIT=True \
    GALAXY_CONFIG_USE_CACHED_DEPENDENCY_MANAGER=True

# Install tools
ADD graphclust.yml $GALAXY_ROOT/tools.yaml
RUN install-tools $GALAXY_ROOT/tools.yaml && \
    /tool_deps/_conda/bin/conda clean --tarballs

ADD ./tours/graphclust_tutorial.yaml $GALAXY_ROOT/config/plugins/tours/graphclust.tutorial.yaml
ADD ./tours/graphclust_step_by_step.yaml $GALAXY_ROOT/config/plugins/tours/graphclust.step_by_step.yaml
ADD ./tours/graphclust_very_short.yaml $GALAXY_ROOT/config/plugins/tours/graphclust.short.yaml

# Data libraries
ADD setup_data_libraries.py $GALAXY_ROOT/setup_data_libraries.py
ADD library_data.yaml $GALAXY_ROOT/library_data.yaml

# Hacky script to import workflows into Galaxy after installation. I would argue this step is redundant.
ADD import_workflows.py $GALAXY_ROOT/import_workflows.py
ADD ./workflows/GraphClust_one.ga $GALAXY_ROOT/GraphClust_one.ga
ADD ./workflows/GraphClust_two.ga $GALAXY_ROOT/GraphClust_two.ga
ADD ./workflows/GraphClust-MotifFinder.ga $GALAXY_ROOT/GraphClust-MotifFinder.ga

# Download training data and populate the data library
RUN startup_lite && \
    sleep 30 && \
    . $GALAXY_VIRTUAL_ENV/bin/activate && \
    python $GALAXY_ROOT/setup_data_libraries.py -i $GALAXY_ROOT/library_data.yaml && \
    python $GALAXY_ROOT/import_workflows.py

# Container Style
ADD workflow_early.png $GALAXY_CONFIG_DIR/web/welcome_image.png
ADD welcome.html $GALAXY_CONFIG_DIR/web/welcome.html

