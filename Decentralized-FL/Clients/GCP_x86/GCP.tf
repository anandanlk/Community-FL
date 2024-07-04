provider "google" {
  project = "melodic-bazaar-425918-r2"
  region  = "europe-west4"
  zone    = "europe-west4-a"
}

variable "client_count" {
  description = "Number of clients to create"
  default     = 8
}

resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
}

resource "google_compute_firewall" "allow-http-and-custom-ports" {
  name    = "allow-http-and-custom-ports"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["80", "3000", "8088", "8000"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow-ssh" {
  name    = "allow-ssh"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_instance" "client" {
  count = var.client_count

  name         = "client-terra-${count.index + 1}"
  machine_type = "e2-medium"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      type  = "pd-ssd"
      size  = 20
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.name

    access_config {
      # This will assign a public IP
    }
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl restart ssh
    mkdir -p /home/fltraining
    cd /home/fltraining
    touch client_id${count.index + 1}.pt
    sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo curl -L -O https://github.com/anandanlk/Compose/raw/main/enumerated_tensors_60_version${count.index + 1}.pth
    sudo curl -O https://raw.githubusercontent.com/anandanlk/Compose/main/client_compose.yml
    sudo /usr/local/bin/docker-compose -f client_compose.yml up -d
  EOF

  tags = ["clients"]

  service_account {
    email  = "default"
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }
}
