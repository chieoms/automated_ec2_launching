import subprocess
import json
import os
import sys

print("Initializing Terraform...")
subprocess.run(["terraform", "init"], cwd="infrastructure")

# Generate SSH keys for Terraform
if os.path.exists("./infrastructure/terraform_key") and os.path.exists("./infrastructure/terraform_key.pub"):
    print("SSH keys already exist. Skipping generation.")
else:
    print("Generating SSH keys...")
    subprocess.run(
        ["ssh-keygen", "-t", "ed25519", "-f", "terraform_key", "-N", ""],
        cwd="infrastructure",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

print("Applying Terraform configuration...")
with open("terraform_build_stdout.log", "w") as out, open("terraform_build_stderr.log", "w") as err:
    terraform_log = subprocess.run(
        ["terraform", "apply", "-auto-approve"],
        cwd = "infrastructure",
        stdout=out,
        stderr=err,
        text=True
    )

if terraform_log.returncode == 0:
    print("Terraform apply completed successfully.")
else:
    print("Terraform apply failed. Check stderr.log for details.")
    sys.exit(1)

print("Logging in to ec2 instance...")
print()
print()

instance_ip = subprocess.run(
    ["terraform", "output", "-json"],
    capture_output=True,
    text=True,
    cwd="infrastructure"
)

if instance_ip.returncode != 0:
    print(instance_ip.stderr)
    raise Exception("Terraform output failed")

outputs = json.loads(instance_ip.stdout)

public_ip = outputs["public_ip"]["value"]

subprocess.run([
    "ssh",
    "-i", "terraform_key",
    "-o", "StrictHostKeyChecking=no",
    "-o", "UserKnownHostsFile=/dev/null",
    f"ubuntu@{public_ip}"
], cwd="infrastructure")