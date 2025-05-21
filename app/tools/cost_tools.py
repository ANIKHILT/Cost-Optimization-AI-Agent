from google.cloud import compute_v1
from datetime import datetime, timedelta
import csv, os
import random

REPORT_BUCKET = os.getenv("REPORT_BUCKET", "")


def _write_report(filename: str, rows: list):
    os.makedirs("reports", exist_ok=True)
    filepath = f"reports/{filename}"
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Resource", "Type", "Action Taken", "Priority", "Timestamp"])
        for row in rows:
            writer.writerow(row)
    return filepath

def list_idle_resources(cloud_provider: str, project_id: str) -> str:
    messages = []
    if cloud_provider == "GCP":
        compute_client = compute_v1.InstancesClient()
        disk_client = compute_v1.DisksClient()
        snapshot_client = compute_v1.SnapshotsClient()

        agg_list = compute_client.aggregated_list(project=project_id)
        for zone, response in agg_list:
            if not hasattr(response, "instances") or response.instances is None:
                continue
            for instance in response.instances:
                if instance.status == "TERMINATED":
                    zone_name = zone.split("/")[-1] if "/" in zone else zone
                    messages.append(f"[TERMINATED] VM: {instance.name} in {zone_name}")
    return "\n".join(messages) or "No idle resources found."

def suggest_optimizations(cloud_provider: str, project_id: str, mode: str) -> str:
    now = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    messages, report_rows = [], []

    if cloud_provider == "GCP":
        compute_client = compute_v1.InstancesClient()
        disk_client = compute_v1.DisksClient()
        snapshot_client = compute_v1.SnapshotsClient()

        agg_list = compute_client.aggregated_list(project=project_id)
        for zone, response in agg_list:
            if not hasattr(response, "instances") or response.instances is None:
                continue
            for instance in response.instances:
                if instance.status == "TERMINATED":
                    zone_name = zone.split("/")[-1] if "/" in zone else zone
                    priority = random.choice(["Low", "Medium", "High"])
                    msg = f"[TERMINATED] VM: {instance.name} in {zone_name} | Priority: {priority}"
                    messages.append(msg)
                    action_taken = "None"
                    if mode == "Execute Actions":
                        try:
                            compute_client.delete(project=project_id, zone=zone_name, instance=instance.name)
                            messages.append(f"✅ Deleted instance: {instance.name}")
                            action_taken = "Deleted"
                        except Exception as e:
                            messages.append(f"❌ Failed to delete {instance.name}: {str(e)}")
                            action_taken = f"Error: {str(e)}"
                    report_rows.append([instance.name, "VM", action_taken, priority, now])

    report_file = f"Cost_Optimizer_Report_{now}.csv"
    filepath = _write_report(report_file, report_rows)
    messages.append(f"\n📄 Report saved to {filepath}")
    return "\n".join(messages) or "No cost optimization opportunities found."
