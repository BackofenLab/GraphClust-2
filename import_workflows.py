#!/usr/bin/env python

import os
from bioblend import galaxy
admin_email = os.environ.get('GALAXY_DEFAULT_ADMIN_USER', 'admin@galaxy.org')
admin_pass = os.environ.get('GALAXY_DEFAULT_ADMIN_PASSWORD', 'admin')
url = "http://localhost:8080"
gi = galaxy.GalaxyInstance(url=url, email=admin_email, password=admin_pass)

wf = galaxy.workflows.WorkflowClient(gi)

for filepath in os.listdir('/home/galaxy/'):
    if filepath.endswith('.ga'):
        wf.import_workflow_from_local_path( os.path.join('/home/galaxy/', filepath) )
