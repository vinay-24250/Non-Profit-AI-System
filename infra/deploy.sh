#!/bin/bash

cd infra/terraform
terraform init
terraform apply -auto-approve

IP=$(terraform output -raw public_ip)

cd ../ansible
echo "[server]" > inventory.ini
echo "$IP ansible_user=ubuntu ansible_ssh_private_key_file=../terraform/key.pem" >> inventory.ini

ansible-playbook deploy.yml