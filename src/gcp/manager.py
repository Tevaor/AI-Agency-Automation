"""
GCP integration manager for handling cloud operations.
"""
from typing import Any, Dict, List, Optional
import logging
from datetime import datetime

from google.cloud.compute_v1.services.instances import InstancesClient
from google.cloud import storage
from google.cloud import monitoring_v3
from google.cloud.logging_v2 import Client as CloudLoggingClient
from google.oauth2 import service_account

logger = logging.getLogger(__name__)

class GCPManager:
    """Manager class for GCP operations."""
    
    def __init__(
        self,
        project_id: str,
        credentials_path: Optional[str] = None,
        region: str = "us-central1"
    ):
        self.project_id = project_id
        self.region = region
        
        # Initialize credentials
        if credentials_path:
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
        else:
            self.credentials = None
        
        # Initialize clients
        if self.credentials or self.project_id:
            self.compute_client = InstancesClient(credentials=self.credentials)
            self.storage_client = storage.Client(
                project=project_id,
                credentials=self.credentials
            )
            self.monitoring_client = monitoring_v3.MetricServiceClient(
                credentials=self.credentials
            )
            self.logging_client = CloudLoggingClient(
                project=project_id,
                credentials=self.credentials
            )
        else:
            # Use mocks for local development/testing without real GCP credentials
            from unittest.mock import MagicMock
            self.compute_client = MagicMock()
            self.storage_client = MagicMock()
            self.monitoring_client = MagicMock()
            self.logging_client = MagicMock()

            # Mock the delete method for compute_client
            self.compute_client.delete.return_value = MagicMock()
            self.compute_client.delete.return_value.result.return_value = None # Simulate successful operation

            # Mock the insert method for compute_client as well to avoid issues during create_vm_instance
            self.compute_client.insert.return_value = MagicMock()
            self.compute_client.insert.return_value.result.return_value = MagicMock(name="mock_operation_name")

            # Mock get_from_family for create_vm_instance
            self.compute_client.get_from_family.return_value = MagicMock(self_link="mock_image_self_link")

            logger.warning("GCPManager initialized without credentials. Using mock clients for local development.")
    
    async def create_vm_instance(
        self,
        instance_name: str,
        machine_type: str,
        zone: str,
        image_family: str = "debian-11",
        image_project: str = "debian-cloud",
        network: str = "default",
        subnetwork: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Create a new VM instance."""
        try:
            # Get the latest image
            image_response = self.compute_client.get_from_family(
                project=image_project,
                family=image_family
            )
            
            # Configure the machine
            machine_type_url = f"zones/{zone}/machineTypes/{machine_type}"
            
            # Configure the network interface
            network_interface = {
                "network": f"projects/{self.project_id}/global/networks/{network}",
                "access_configs": [{"name": "External NAT", "type": "ONE_TO_ONE_NAT"}]
            }
            if subnetwork:
                network_interface["subnetwork"] = f"regions/{self.region}/subnetworks/{subnetwork}"
            
            # Create the instance
            instance = compute_v1.Instance(
                name=instance_name,
                machine_type=machine_type_url,
                network_interfaces=[network_interface],
                disks=[
                    {
                        "boot": True,
                        "auto_delete": True,
                        "initialize_params": {
                            "source_image": image_response.self_link,
                            "disk_size_gb": "10"
                        }
                    }
                ],
                tags=compute_v1.Tags(items=tags or []),
                metadata=compute_v1.Metadata(items=[
                    {"key": k, "value": v} for k, v in (metadata or {}).items()
                ])
            )
            
            operation = self.compute_client.insert(
                project=self.project_id,
                zone=zone,
                instance_resource=instance
            )
            
            # Wait for the operation to complete
            operation.result()
            
            return {
                "status": "success",
                "instance_name": instance_name,
                "zone": zone,
                "operation_id": operation.name
            }
        except Exception as e:
            logger.error(f"Failed to create VM instance: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def delete_vm_instance(
        self,
        instance_name: str,
        zone: str
    ) -> Dict[str, Any]:
        """Delete a VM instance."""
        try:
            operation = self.compute_client.delete(
                project=self.project_id,
                zone=zone,
                instance=instance_name
            )
            
            # Wait for the operation to complete
            operation.result()
            
            return {
                "status": "success",
                "instance_name": instance_name,
                "zone": zone,
                "operation_id": operation.name
            }
        except Exception as e:
            logger.error(f"Failed to delete VM instance: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def create_storage_bucket(
        self,
        bucket_name: str,
        location: Optional[str] = None,
        storage_class: str = "STANDARD",
        labels: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Create a new storage bucket."""
        try:
            bucket = self.storage_client.bucket(bucket_name)
            bucket.create(
                location=location or self.region,
                storage_class=storage_class,
                labels=labels
            )
            
            return {
                "status": "success",
                "bucket_name": bucket_name,
                "location": location or self.region
            }
        except Exception as e:
            logger.error(f"Failed to create storage bucket: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def delete_storage_bucket(
        self,
        bucket_name: str,
        force: bool = False
    ) -> Dict[str, Any]:
        """Delete a storage bucket."""
        try:
            bucket = self.storage_client.bucket(bucket_name)
            bucket.delete(force=force)
            
            return {
                "status": "success",
                "bucket_name": bucket_name
            }
        except Exception as e:
            logger.error(f"Failed to delete storage bucket: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def get_metrics(
        self,
        metric_type: str,
        interval: Dict[str, str],
        filter_str: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get metrics from Cloud Monitoring."""
        try:
            project_name = f"projects/{self.project_id}"
            
            # Create the time interval
            time_interval = monitoring_v3.TimeInterval(
                start_time=datetime.fromisoformat(interval["start_time"]),
                end_time=datetime.fromisoformat(interval["end_time"])
            )
            
            # Create the request
            request = monitoring_v3.ListTimeSeriesRequest(
                name=project_name,
                filter=filter_str or f'metric.type = "{metric_type}"',
                interval=time_interval,
                view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
            )
            
            # Make the request
            results = self.monitoring_client.list_time_series(request=request)
            
            return {
                "status": "success",
                "metric_type": metric_type,
                "data": [ts for ts in results]
            }
        except Exception as e:
            logger.error(f"Failed to get metrics: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def write_log_entry(
        self,
        log_name: str,
        text_payload: str,
        severity: str = "INFO",
        labels: Optional[Dict[str, str]] = None,
        resource: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Write a log entry to Cloud Logging."""
        try:
            logger = self.logging_client.logger(log_name)
            
            # Create the log entry
            entry = cloud_logging.LogEntry(
                text_payload=text_payload,
                severity=severity,
                labels=labels,
                resource=resource
            )
            
            # Write the log entry
            logger.write_entries([entry])
            
            return {
                "status": "success",
                "log_name": log_name,
                "severity": severity
            }
        except Exception as e:
            logger.error(f"Failed to write log entry: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def list_resources(
        self,
        resource_type: str,
        filter_str: Optional[str] = None
    ) -> Dict[str, Any]:
        """List GCP resources of a specific type."""
        try:
            if resource_type == "instances":
                request = compute_v1.ListInstancesRequest(
                    project=self.project_id,
                    zone=self.region
                )
                response = self.compute_client.list(request=request)
                resources = [instance for instance in response]
            elif resource_type == "buckets":
                resources = [bucket for bucket in self.storage_client.list_buckets()]
            else:
                raise ValueError(f"Unsupported resource type: {resource_type}")
            
            return {
                "status": "success",
                "resource_type": resource_type,
                "resources": resources
            }
        except Exception as e:
            logger.error(f"Failed to list resources: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            } 