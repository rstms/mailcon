terraform {
  required_providers {
    cloudsigma = {
      source = "cloudsigma/cloudsigma"
      version = "1.4.2"
    }
  }
}

variable "SERVER_NAME" { type = string }
variable "CLOUDSIGMA_USERNAME" { type = string }
variable "CLOUDSIGMA_PASSWORD" { type = string }
variable "CPU" { type = number }
variable "DISK" { type = number }
variable "MEMORY" { type = number }
variable "VNC_PASSWORD" { type = string }


# Configure the CloudSigma Provider
provider "cloudsigma" {
  username = var.CLOUDSIGMA_USERNAME
  password = var.CLOUDSIGMA_PASSWORD
}

#resource "cloudsigma_ssh_key" "public_key" {
#  name       = var.SERVER_NAME
#  public_key = file( "${var.SERVER_NAME}.pub" )
#}

data "cloudsigma_library_drive" "install" {
  filter = {
    name   = "openbsd_install_cd"
    values = ["OpenBSD 6.9 Install CD"]
  }
}

resource "cloudsigma_drive" "data" {
  media = "disk"
  name  = "home"
  size  = var.DISK * 1024 * 1024 * 1024 # GB
}

# Create a server
resource "cloudsigma_server" "server" {
  name         = var.SERVER_NAME
  cpu          = var.CPU
  memory       = var.MEMORY * 1024 * 1024 * 1024 # GB
  vnc_password = var.VNC_PASSWORD
  drive {      
    uuid = coudsigma_library_drive.install.id
    uuid = cloudsigma_drive.data.id
  }
}
