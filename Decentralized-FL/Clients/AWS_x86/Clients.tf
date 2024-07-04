provider "aws" {
  region = "eu-north-1"
}
variable "client_count" {
  description = "Number of clients to create"
  default     = 2
}

data "aws_security_group" "existing" {
  id = "sg-0f7a504c17e832352"
}

resource "aws_instance" "client" {
  count = var.client_count

  ami           = "ami-01dad638e8f31ab9a"
  instance_type = "t3.small"

  key_name = "server"

  tags = {
    "Name" = "ClientTerra${count.index + 1}"
  }

  vpc_security_group_ids = [data.aws_security_group.existing.id]

  credit_specification {
    cpu_credits = "standard"
  }

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker
    yum install -y php-curl
    service docker start
    cd /home/ec2-user
    touch client_id${count.index + 1}.pt
    sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo curl -L -O https://github.com/anandanlk/Compose/raw/main/enumerated_tensors_5_version${count.index + 1}.pth
    sudo curl -O https://raw.githubusercontent.com/anandanlk/Compose/main/client_compose.yml
    sudo docker-compose -f client_compose.yml up -d
  EOF

  root_block_device {
    volume_type           = "gp3"
    volume_size           = 15
    delete_on_termination = true
    iops                  = 3000
  }
}
