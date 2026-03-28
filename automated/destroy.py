import subprocess
import os

print("Destroying Terraform-managed infrastructure...")

with open("terraform_destroy_stdout.log", "w") as out, open("terraform_destroy_stderr.log", "w") as err:
    terraform_log = subprocess.run(
        ["terraform", "destroy", "-auto-approve"],
        cwd = "infrastructure",
        stdout=out,
        stderr=err,
        text=True
    )


print("Removing generated SSH keys...")

# Comment out if you are running on Windows without Git Bash, WSL or Linux.
for file in ["terraform_key", "terraform_key.pub"]:
    path = os.path.join("infrastructure", file)
    if os.path.exists(path):
        os.remove(path) 

# uncomment if you running on Linux or with Git Bash on Windows.
# subprocess.run(["rm", "-f", "terraform_key", "terraform_key.pub"], cwd="infrastructure")

print("Terraform destroy completed. \nCheck terraform_destroy_stdout.log and terraform_destroy_stderr.log for details.")
