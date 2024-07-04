
provider "aws" {
  region = "eu-north-1"
}

data "aws_security_group" "existing" {
  id = "sg-0f7a504c17e832352"
}


resource "aws_instance" "communication_server" {
  # x86
  ami           = "ami-0c0e147c706360bd7"
  instance_type = "t3.micro"
  key_name      = "server"

  tags = {
    "Name" = "Communication_server_terraform"
  }

  vpc_security_group_ids = [data.aws_security_group.existing.id]



  credit_specification {
    cpu_credits = "standard"
  }

  user_data = <<-EOF
      #!/bin/bash
      yum update -y
      yum install -y docker
      service docker start
      docker pull anandanlk/federation_server_endpoint_test:latest
      sudo docker run -p 8088:8088 -d anandanlk/federation_server_endpoint_test:latest 
  EOF

  root_block_device {
    volume_type           = "gp3"
    volume_size           = 8
    delete_on_termination = true
    iops                  = 3000 # Replace with your desired IOPS (optional)
  }

}
output "CommunicationServerIpDecentralized" {
  description = "CommunicationServer Public IP"
  value       = aws_instance.communication_server.public_ip
}
