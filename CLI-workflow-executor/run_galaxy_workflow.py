#!/usr/bin/env python
"""run_galaxy_workflow

This script run workflows on galaxy instance using credentials.yml file provided.
The input data (barcodes.tsv, genes.tsv, matrix.mtx and gtf) files are upload from
provisioned locally in a directory. This scripts connects to galaxy instance and select the workflow of interest.

running syntax

python run_galaxy_workflow.py -C galaxy_credentials.yml -o output_dir -G 'embassy' -H 'scanpy_param_test' \
       -i inputs.yaml \
       -W Galaxy-Workflow-Scanpy_default_params.json \
       -P scanpy_param_pretty.json

File inputs.yaml must contain paths to all input labels in the workflow.
"""

import argparse
import logging
import os.path
import time
import yaml
from sys import exit
import pickle
import copy
import json
from bioblend.galaxy import GalaxyInstance


def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-C', '--conf',
                            required=True,
                            help='A yaml file describing the galaxy credentials')
    arg_parser.add_argument('-G', '--galaxy-instance',
                            default='embassy',
                            help='Galaxy server instance name')
    arg_parser.add_argument('-i', '--yaml-inputs-path',
                            required=True,
                            help='Path to Yaml detailing inputs')
    arg_parser.add_argument('-o', '--output-dir',
                            default=os.getcwd(),
                            help='Path to output directory')
    arg_parser.add_argument('-H', '--history',
                            default='',
                            required=True,
                            help='Name of the history to create')
    arg_parser.add_argument('-W', '--workflow',
                            required=True,
                            help='Workflow to run')
    arg_parser.add_argument('-P', '--parameters',
                            default='',
                            required=True,
                            help='scanpy parameters json')
    arg_parser.add_argument('--debug',
                            action='store_true',
                            default=False,
                            help='Print debug information')
    arg_parser.add_argument('-a', '--allowed-errors',
                            required=False,
                            default=None,
                            help="Yaml file with allowed steps that can have errors."
                            )
    arg_parser.add_argument('-k', '--keep-histories',
                            action='store_true',
                            default=False,
                            help="Keeps histories created, they will be purged if not.")
    arg_parser.add_argument('-w', '--keep-workflow',
                            action='store_true',
                            default=False,
                            help="Keeps workflow created, it will be purged if not.")
    args = arg_parser.parse_args()
    return args


def set_logging_level(debug=False):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%d-%m-%y %H:%M:%S')


def read_yaml_file(yaml_path):
    """
    Reads a YAML file safely.

    :param yaml_path:
    :return: dictionary object from YAML content.
    """
    stream = open(yaml_path, "r")
    return yaml.safe_load(stream)


def get_instance(conf, name='__default'):
    data = read_yaml_file(os.path.expanduser(conf))
    assert name in data, 'unknown instance'
    entry = data[name]
    if isinstance(entry, dict):
        return entry
    else:
        return data[entry]


def get_workflow_from_file(gi, workflow_file):
    import_workflow = [gi.workflows.import_workflow_from_local_path(file_local_path=workflow_file)]
    return import_workflow


def read_json_file(json_file_path):
    with open(json_file_path) as json_file:
        json_obj = json.load(json_file)
    return json_obj


def get_workflow_from_name(gi, workflow_name):
    wf = gi.workflows.get_workflows(name=workflow_name)
    return wf


def get_history_id(history_name, histories_obj):
    for hist_dict in histories_obj:
        if hist_dict['name'] == history_name:
            return hist_dict['id']


def get_workflow_id(wf):
    for wf_dic in wf:
        wf_id = wf_dic['id']
    return wf_id


def get_input_data_id(file, wf):
    file_name = os.path.splitext(file)[0]
    for id in wf['inputs']:
        if wf['inputs'][id]['label'] == file_name:
            input_id = id
    return input_id


def get_run_state(gi, results):
    results_hid = gi.histories.show_history(results['history_id'])
    state = results_hid['state']
    return state


def download_results(gi, history_id, output_dir, allowed_error_states, use_names=False):
    """
    Downloads results from a given Galaxy instance and history to a specified filesystem location.

    :param gi: galaxy instance object
    :param history_id: ID of the history from where results should be retrieved.
    :param output_dir: path to where result file should be written.
    :param allowed_error_states: dictionary with elements known to be allowed to fail.
    :param use_names: whether to trust or not the internal Galaxy name for the final file name
    :return:
    """
    datasets = gi.histories.show_history(history_id,
                                         contents=True,
                                         visible=True, details='all')
    used_names = set()
    for dataset in datasets:
        if dataset['type'] == 'file':
            if dataset['id'] in allowed_error_states['datasets']:
                logging.info('Skipping download of {} as it is an allowed failure.'
                             .format(dataset['name']))
                continue
            if use_names and dataset['name'] is not None and dataset['name'] not in used_names:
                gi.datasets.download_dataset(dataset['id'], file_path=os.path.join(output_dir, dataset['name']),
                                             use_default_filename=False)
                used_names.add(dataset['name'])
            else:
                gi.datasets.download_dataset(dataset['id'],
                                             file_path=output_dir,
                                             use_default_filename=True)
        elif dataset['type'] == 'collection':
            for ds_in_coll in dataset['elements']:
                if ds_in_coll['object']['id'] in allowed_error_states['datasets']:
                    logging.info('Skipping download of {} as it is an allowed failure.'
                                 .format(ds_in_coll['object']['name']))
                    continue
                if use_names and ds_in_coll['object']['name'] is not None \
                        and ds_in_coll['object']['name'] not in used_names:
                    # TODO it fails here to download if it is in 'error' state
                    gi.datasets.download_dataset(ds_in_coll['object']['id'],
                                                 file_path=os.path.join(output_dir, ds_in_coll['object']['name']),
                                                 use_default_filename=False)
                    used_names.add(ds_in_coll['object']['name'])
                else:
                    gi.datasets.download_dataset(ds_in_coll['object']['id'],
                                                 file_path=output_dir,
                                                 use_default_filename=True)


def set_params(json_wf, param_data):
    """
    Associate parameters to workflow steps via the step label. The result is a dictionary
    of parameters that can be passed to invoke_workflow.

    :param json_wf:
    :param param_data:
    :return:
    """
    params = {}
    for param_step_name in param_data:
        step_ids = (key for key, value in json_wf['steps'].items() if value['label'] == str(param_step_name))
        for step_id in step_ids:
            params.update({step_id: param_data[param_step_name]})
        for param_name in param_data[param_step_name]:
            if '|' in param_name:
                logging.warning("Workflow using Galaxy <repeat /> "
                                "param. type for {} / {}. "
                                "Make sure that workflow has as many entities of that repeat "
                                "as they are being set in the parameters file.".format(param_step_name, param_name))
                break
    return params


def load_input_files(gi, inputs, workflow, history):
    """
    Loads file in the inputs yaml to the Galaxy instance given. Returns
    datasets dictionary with names and histories. It associates existing datasets on Galaxy given by dataset_id
    to the input where they should be used.

    This setup currently doesn't support collections as inputs.

    Input yaml file should be formatted as:

    input_label_a:
      path: /path/to/file_a
      type:
    input_label_b:
      path: /path/to/file_b
      type:
    input_label_c:
      dataset_id:

    this makes it extensible to support
    :param gi: the galaxy instance (API object)
    :param inputs: dictionary of inputs as read from the inputs YAML file
    :param workflow: workflow object produced by gi.workflows.show_workflow
    :param history: the history object to where the files should be uploaded
    :return: inputs object for invoke_workflow
    """

    inputs_for_invoke = {}

    for step, step_data in workflow['inputs'].items():
        # upload file and record the identifier
        if step_data['label'] in inputs and 'path' in inputs[step_data['label']]:
            upload_res = gi.tools.upload_file(path=inputs[step_data['label']]['path'], history_id=history['id'],
                                              file_name=step_data['label'],
                                              file_type=inputs[step_data['label']]['type'])
            inputs_for_invoke[step] = {
                    'id': upload_res['outputs'][0]['id'],
                    'src': 'hda'
                }
        elif step_data['label'] in inputs and 'dataset_id' in inputs[step_data['label']]:
            inputs_for_invoke[step] = {
                'id': inputs[step_data['label']]['dataset_id'],
                'src': 'hda'
            }
        else:
            raise ValueError("Label '{}' is not present in inputs yaml".format(step_data['label']))

    return inputs_for_invoke


def validate_labels(wf_from_json, param_data, exit_on_error=True):
    """
    Checks that all workflow steps have labels (although if not the case, it will only
    warn that those steps won't be configurable for parameters) and that all step labels
    in the parameter files exist in the workflow file. If the second case is not true,
    the offending parameter is shown and the program exists.

    :param wf_from_json:
    :param param_data:
    :param exit_on_error:
    :return:
    """
    step_labels_wf = []
    for step_id, step_content in wf_from_json['steps'].items():
        if step_content['label'] is None:
            logging.warning("Step No {} in json workflow does not have a label, parameters are not mappable there.".format(step_id))
        step_labels_wf.append(step_content['label'])
    errors = 0
    for step_label_p, params in param_data.items():
        if step_label_p not in step_labels_wf:
            if exit_on_error:
                raise ValueError(
                    " '{}' parameter step label is not present in the workflow definition".format(step_label_p))
            logging.error("{} parameter step label is not present in the workflow definition".format(step_label_p))
            errors += 1
    if errors == 0:
        logging.info("Validation of labels: OK")


def validate_input_labels(wf_json, inputs):
    """
    Check that all input datasets in the workflow have labels, and that those labels are available in the inputs yaml.
    Raises an exception if those cases are not fulfilled.

    :param wf_json:
    :param inputs:
    :return: the number of input labels.
    """

    number_of_inputs = 0
    for step, step_content in wf_json['steps'].items():
        if step_content['type'] == 'data_input':
            number_of_inputs += 1
            if step_content['label'] is None:
                raise ValueError("Input step {} in workflow has no label set.".format(str(step)))

            if step_content['label'] not in inputs:
                raise ValueError("Input step {} label {} is not present in the inputs YAML file provided."
                                 .format(str(step), step_content['label']))
    return number_of_inputs


def validate_file_exists(inputs):
    """
    Checks that paths exists in the local file system.

    :param inputs: dictionary with inputs
    :return:
    """
    for input_key, input_content in inputs.items():
        if 'path' in input_content and not os.path.isfile(input_content['path']):
            raise ValueError("Input file {} does not exist for input label {}".format(input_content['path'], input_key))


def validate_dataset_id_exists(gi, inputs):
    """
    Checks that dataset_id exists in the Galaxy instance when dataset_id are specified. Raises an error if the dataset
    id doesn't exists in the instance.

    :param gi:
    :param inputs:
    :return:
    """
    warned = False
    for input_key, input_content in inputs.items():
        if 'dataset_id' in input_content:
            ds_in_instance = gi.datasets.show_dataset(dataset_id=input_content['dataset_id'])
            if not warned:
                logging.warning("You are using direct dataset identifiers for inputs, "
                                "this execution is not portable accross instances.")
                warned = True
            if not isinstance(ds_in_instance, dict):
                raise ValueError("Input dataset_id {} does not exist in the Galaxy instance."
                                 .format(input_content['dataset_id']))


def completion_state(gi, history, allowed_error_states, wait_for_resubmission=True):
    """
    Checks whether the history is in error state considering potential acceptable error states
    in the allowed error states definition.

    :param wait_for_resubmission:
    :param gi: The galaxy instance connection
    :param history:
    :param allowed_error_states: dictionary containing acceptable error states for steps
    :return: two booleans, error_state and completed
    """

    # First easy check for error state if there are no allowed errors
    error_state = len(allowed_error_states['tools']) == 0 and history['state_details']['error'] > 0

    # If there are allowed error states, check details
    if not error_state:
        for dataset_id in history['state_ids']['error']:
            if dataset_id in allowed_error_states['datasets']:
                continue
            dataset = gi.datasets.show_dataset(dataset_id)
            job = gi.jobs.show_job(dataset['creating_job'])
            if job['tool_id'] in allowed_error_states['tools']:
                allowed_error_states['datasets'].add(dataset_id)
                # TODO decide based on individual error codes.
                continue
            logging.info("Tool {} is not marked as allowed to fail, but has failed.".format(job['tool_id']))
            # Sometimes transient error states will be found for jobs that are in the process
            # of being resubmitted. This part accounts for that, waiting for the state to go back
            # from error.
            if wait_for_resubmission:
                # We have seen jobs circling from error to running again in lapses of around 10 seconds
                # at the most, so we wait for conservative period. This could be improved later.
                logging.info("Waiting 20 sec to check if the job gets re-submitted")
                time.sleep(20)
                ds = gi.datasets.show_dataset(dataset_id)
                if not ds['resubmitted']:
                    logging.info("Job was not resubmitted")
                    error_state = True
                    break
                elif ds['state'] != 'error':
                    logging.info("Job was resubmitted and is not in error any more...")
                else:
                    logging.info("Job was resubmitted at some point, but still shows to be in error state, failing")
                    error_state = True
                    break
            else:
                error_state = True
                break

    # We separate completion from errors, so a workflow might have completed with or without errors
    # (this includes allowed errors). We say the workflow is in completed state when all datasets are in states:
    # error, ok, paused or failed_metadata.
    terminal_states = ['error', 'ok', 'paused', 'failed_metadata']
    non_terminal_datasets_count = 0
    terminal_datasets_count = 0
    for state, count in history['state_details'].items():
        if state not in terminal_states:
            non_terminal_datasets_count += count
        if state in terminal_states:
            terminal_datasets_count += count

    # We add the terminal_datasets_count to avoid falling here when all job states are in zero.
    completed_state = (non_terminal_datasets_count == 0 and terminal_datasets_count > 0)

    if completed_state:
        # add all paused jobs to allowed_error_states or fail if jobs are paused that are not allowed
        for dataset_id in history['state_ids']['paused']:
            dataset = gi.datasets.show_dataset(dataset_id)
            job = gi.jobs.show_job(dataset['creating_job'])
            if job['tool_id'] in allowed_error_states['tools']:
                allowed_error_states['datasets'].add(dataset_id)
                # TODO decide based on individual error codes.
                continue
            logging.info("Tool {} is not marked as allowed to fail, but is paused due to a previous tool failure."
                         .format(job['tool_id']))
            error_state = True
        # display state of jobs in history:
        logging.info("Workflow run has completed, job counts per states are:")
        for state, count in history['state_details'].items():
            logging.info("{}: {}".format(state, count))

    return error_state, completed_state


def process_allowed_errors(allowed_errors_dict, wf_from_json):
    """
    Reads the input from allowed errors file and translates the workflow steps into tool identifiers that will be
    allowed to error out, either on all error codes (when "any" is available for the tool) or on specified error codes.

    :param wf_from_json:
    :param allowed_errors_dict: content from yaml file with definition of steps can fail.
    :return:
    """

    allowed_errors_state = {'tools': {}, 'datasets': set()}
    for step_id, step_content in wf_from_json['steps'].items():
        if step_content['label'] is not None and step_content['tool_id'] is not None:
            if step_content['label'] in allowed_errors_dict:
                allowed_errors_state['tools'][step_content['tool_id']] = allowed_errors_dict[step_content['label']]

    return allowed_errors_state


def produce_versions_file(gi, workflow_from_json, path):
    """
    Produces a tool versions file for the workflow run.

    :param gi:
    :param workflow_from_json:
    :param path: path where to save the versions file
    :return:
    """

    tools_dict = []

    with open(file=path, mode="w") as f:
        f.write("\t".join(["Analysis", "Software", "Version", "Citation"])+"\n")

        for key, step in sorted(workflow_from_json['steps'].items(), reverse=True):
            # Input steps won't have tool ids, and we only need each tool once.
            if step['tool_id'] is not None and step['tool_id'] not in tools_dict:
                tool = gi.tools.show_tool(step['tool_id'])
                label = step['label'] if step['label'] is not None else tool['name']
                url = ""
                if tool['tool_shed_repository'] is not None:
                    ts_meta = tool['tool_shed_repository']
                    url = "https://{}/view/{}/{}/{}".format(ts_meta['tool_shed'], ts_meta['owner'], ts_meta['name'],
                                                            ts_meta['changeset_revision'])
                f.write("\t".join([label, tool['name'], tool['version'], url])+"\n")
                tools_dict.append(step['tool_id'])
                # tools_dict[step['tool_id']] = {'name': tool['name'], 'version': tool['version']}


def main():
    try:
        args = get_args()
        set_logging_level(args.debug)

        # Load workflows, inputs and parameters
        wf_from_json = read_json_file(args.workflow)
        param_data = read_json_file(args.parameters)
        inputs_data = read_yaml_file(args.yaml_inputs_path)
        allowed_error_states = {'tools': {}, 'datasets': set()}
        if args.allowed_errors is not None:
            allowed_error_states = \
                process_allowed_errors(read_yaml_file(args.allowed_errors), wf_from_json)


        # Validate data before talking to Galaxy
        validate_labels(wf_from_json, param_data)
        num_inputs = validate_input_labels(wf_json=wf_from_json, inputs=inputs_data)
        if num_inputs > 0:
            validate_file_exists(inputs_data)

        # Prepare environment and do any post connection validations.
        logging.info('Prepare galaxy environment...')
        ins = get_instance(args.conf, name=args.galaxy_instance)
        gi = GalaxyInstance(ins['url'], key=ins['key'])
        validate_dataset_id_exists(gi, inputs_data)

        # Create new history to run workflow
        logging.info('Create new history to run workflow ...')
        if num_inputs > 0:
            history = gi.histories.create_history(name=args.history)

        # get saved workflow defined in the galaxy instance
        logging.info('Workflow setup ...')
        workflow = get_workflow_from_file(gi, workflow_file=args.workflow)
        workflow_id = get_workflow_id(wf=workflow)
        show_wf = gi.workflows.show_workflow(workflow_id)

        # upload dataset to history
        logging.info('Uploading dataset to history ...')
        if num_inputs > 0:
            datamap = load_input_files(gi, inputs=inputs_data,
                                       workflow=show_wf, history=history)
        else:
            datamap = {}
        # set parameters
        logging.info('Set parameters ...')
        params = set_params(wf_from_json, param_data)

        try:
            logging.info('Running workflow {}...'.format(show_wf['name']))
            results = gi.workflows.invoke_workflow(workflow_id=workflow_id,
                                                   inputs=datamap,
                                                   params=params,
                                                   history_name=(args.history + '_results'))
        except Exception as ce:
            logging.error("Failure when invoking invoke workflows: {}".format(str(ce)))
            raise ce

        logging.debug("About to start serialization...")
        try:
            res_file_path = os.path.join(args.output_dir, args.history + '_results.bin')
            binary_file = open(res_file_path, mode='wb')
            pickle.dump(results, binary_file)
            binary_file.close()
            logging.info("State serialized for recovery at {}".format(str(res_file_path)))
        except Exception as e:
            logging.error("Failed to serialize (skipping)... {}".format(str(e)))

        # Produce tool versions file
        produce_versions_file(gi=gi, workflow_from_json=wf_from_json,
                              path="{}/software_versions_galaxy.txt".format(args.output_dir))

        # wait for a little while and check if the status is ok
        logging.info("Waiting for results to be available...")
        logging.info("...in the mean time, you can check {}/histories/view?id={} for progress."
                     "You need to login with the user that owns the API Key.".
                     format(gi.base_url, results['history_id']))
        time.sleep(100)

        # get_run_state
        results_hid = gi.histories.show_history(results['history_id'])
        state = results_hid['state']

        # wait until workflow invocation is fully scheduled, cancelled of failed
        while True:
            invocation = gi.workflows.show_invocation(workflow_id=results['workflow_id'], invocation_id=results['id'])
            if invocation['state'] in ['scheduled', 'cancelled', 'failed']:
                # These are the terminal states of the invocation process. Scheduled means that all jobs needed for the
                # workflow have been scheduled, not that the workflow is finished. However, there is no point in
                # checking completion through history elements if this hasn't happened yet.
                logging.info("Workflow invocation has entered a terminal state: {}".format(invocation['state']))
                logging.info("Proceeding to check individual jobs state to determine completion or failure...")
                break
            time.sleep(10)

        # wait until the jobs are completed, once workflow scheduling is done.
        logging.debug("Got state: {}".format(state))
        while True:
            logging.debug("Got state: {}".format(state))
            error_state, finalized_state = completion_state(gi, results_hid, allowed_error_states)
            # TODO could a resubmission be caught here in the 'error' state?
            if error_state:
                logging.error("Execution failed, see {}/histories/view?id={} for input details."
                              "You might require login with a particular user.".
                              format(gi.base_url, results_hid['id']))
                exit(1)
            elif finalized_state:
                logging.info("Workflow finished successfully OK or with allowed errors.")
                break
            # TODO downloads could be triggered here to gain time.
            time.sleep(10)
            results_hid = gi.histories.show_history(results['history_id'])
            state = results_hid['state']

        # Download results
        logging.info('Downloading results ...')
        download_results(gi, history_id=results['history_id'],
                         output_dir=args.output_dir, allowed_error_states=allowed_error_states,
                         use_names=True)
        logging.info('Results available.')

        if not args.keep_histories:
            logging.info('Deleting histories...')
            gi.histories.delete_history(results['history_id'], purge=True)
            if num_inputs > 0:
                gi.histories.delete_history(history['id'], purge=True)
            logging.info('Histories purged...')

        if not args.keep_workflow:
            logging.info('Deleting workflow...')
            gi.workflows.delete_workflow(workflow_id=workflow_id)
            logging.info('Workflow deleted.')

        exit(0)
    except Exception as e:
        logging.error("Failed due to {}".format(str(e)))
        raise e


if __name__ == '__main__':
    main()



