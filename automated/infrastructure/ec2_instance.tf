provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "terraform_ec2_instance" {
  ami                    = "ami-0ec10929233384c7f"
  instance_type          = "t2.micro"
  availability_zone      = "us-east-1c"
  key_name =  aws_key_pair.terraform_key_pair.key_name
  vpc_security_group_ids = [aws_security_group.terraform_sg.id]

  tags = {
    Name = "terraform-ec2-instance"
  }
}

resource "aws_key_pair" "terraform_key_pair" {
  key_name   = "terraform_key"
  public_key = file("terraform_key.pub")
}

output "public_ip" {
  value = aws_instance.terraform_ec2_instance.public_ip
}