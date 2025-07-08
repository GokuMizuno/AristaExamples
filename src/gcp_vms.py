from __future__ import annotations
from collections import defaultdict
from collections.abc import Iterable
from google.cloud import compute_v1
from src import gcp_base
# from google.api_core.extended_operation import ExtendedOperation
# from google.cloud import compute_v1
import requests


class gcp_VMs(gcp_base):
    def __init__():
        super().__init__()

    def getVMList(self, project_id: str, zone="") -> dict[str, Iterable[compute_v1.Instance]]:
        """
        This gets all the VMs associated with a given GCP account,
        across all zones if a zone is not given

        Args:
            project_id (str):  The project id
            zone (str): optional, but retuns only the vms for that zone

        Returns:
            VMs (dict): All the VMs associated with a given project ID

        Raises:
            Exception if something goes wrong
        """
        # We use the gcp specific endpoints to get all VMs and statuses
        iclient = compute_v1.InstancesClient()
        if zone != "":
            try:
                ilist = iclient.list(project=project_id, zone=zone)
                return ilist
            except Exception as e:
                print(f"Exception in getting {zone} VMs: {str(e)}")
                # return {"zone": []}
                raise
        else:
            # All the ZONES!
            request = compute_v1.AggregatedListInstancesRequest()
            request.project = project_id
            # request.max_results = 50  # Google recommended.  Uncomment for pagination
            aggregate_list = iclient.aggregated_list(request)
            full_list = defaultdict(aggregate_list)
            return full_list
        
    def get_vm_details(self, project_id: str, zone: str, vm_name: str):
        '''
        Gets the details of a given VM in a zone
        Presumes you have the Compute Instance Admin (v1) role, otherwise, returns 402 status

        Args:
            project_id (str):  The project id
            zone (str): the zone
            vm_name (str): The VM's name

        Returns:
            VM_details (json): All the details associated with a given VM

        Raises:
            Exception if something goes wrong
        '''
        url = f"https://compute.googleapis.com/compute/v1/projects/{project_id}/zones/{zone}/instances/{vm_name}"
        response = requests.get(url)
        if response:
            # Should this be trimmed down?
            return response
        else:
            raise Exception(f"Bad Response, code {response.status_code}")

    def get_vm_UUID(self, project_id: str, zone: str, vm_name: str):
        pass

    def create_vm(self):
        pass

    def shutdown_vm(self, project_id: str, zone: str, instance_name, discardData="false"):
        # POST 
        url = f"https://compute.googleapis.com/compute/beta/projects/{project_id}/zones/{zone}/instances/{instance_name}/stop?discardLocalSsd={discardData}"
        requests.post(url=url)
        # TODO:  FINISH THIS!

    def shutdown_vm_with_data_destruction(self, project_id: str, zone: str, instance_name):
        self.shutdown_vm(project_id, zone, instance_name, "true")

    def destroy_vm_and_data(self, project_id: str, zone: str, instance_name: str):
        # DELETE
        url = f"https://compute.googleapis.com/compute/v1/projects/{project_id}/zones/{zone}/instances/{instance_name}"
        requests.delete(url=url)
        # TODO:  FINISH THIS!

    # def wait_for_extended_operation(
    #     operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
    # ) -> Any:
    #     """
    #     Waits for the extended (long-running) operation to complete.

    #     If the operation is successful, it will return its result.
    #     If the operation ends with an error, an exception will be raised.
    #     If there were any warnings during the execution of the operation
    #     they will be printed to sys.stderr.

    #     Args:
    #         operation: a long-running operation you want to wait on.
    #         verbose_name: (optional) a more verbose name of the operation,
    #             used only during error and warning reporting.
    #         timeout: how long (in seconds) to wait for operation to finish.
    #             If None, wait indefinitely.

    #     Returns:
    #         Whatever the operation.result() returns.

    #     Raises:
    #         This method will raise the exception received from `operation.exception()`
    #         or RuntimeError if there is no exception set, but there is an `error_code`
    #         set for the `operation`.

    #         In case of an operation taking longer than `timeout` seconds to complete,
    #         a `concurrent.futures.TimeoutError` will be raised.
    #     """
    #     result = operation.result(timeout=timeout)

    #     if operation.error_code:
    #         print(
    #             f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
    #             file=sys.stderr,
    #             flush=True,
    #         )
    #         print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
    #         raise operation.exception() or RuntimeError(operation.error_message)

    #     if operation.warnings:
    #         print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
    #         for warning in operation.warnings:
    #             print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    #     return result


    # def stop_instance(project_id: str, zone: str, instance_name: str) -> None:
    #     """
    #     Stops a running Google Compute Engine instance.
    #     Args:
    #         project_id: project ID or project number of the Cloud project your instance belongs to.
    #         zone: name of the zone your instance belongs to.
    #         instance_name: name of the instance your want to stop.
    #     """
    #     instance_client = compute_v1.InstancesClient()

    #     operation = instance_client.stop(
    #         project=project_id, zone=zone, instance=instance_name
    #     )
    #     wait_for_extended_operation(operation, "instance stopping")
