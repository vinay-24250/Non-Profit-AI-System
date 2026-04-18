variable "region" {
  description = "AWS region"
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t3.micro"
}

variable "ami_id" {
  description = "Ubuntu AMI ID (Mumbai region)"
  default     = "ami-03f4878755434977f"
}

variable "key_name" {
  description = "AWS key pair name"
}

variable "instance_name" {
  description = "Name of EC2 instance"
  default     = "nonprofit-server"
}