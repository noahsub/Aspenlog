# Aspenlog 2020 Guide
This guide is meant to provide instructions on how to set up and run the Aspenlog 2020 backend. Due to the complexity of
the backend, it is strongly recommended that you have a basic understanding of Linux and computer networks before
continuing.
## Setting Up the Server Environment
### Prerequisites
You must run the backend on a linux server. If you are using a Windows machine, you can use the Windows Subsystem for
Linux (WSL). You can find more information on how to install WSL 
[here](https://learn.microsoft.com/en-us/windows/wsl/install). If you already have a server, you can skip to the next
section, however, if you do not have a server, you can use a cloud service such as AWS, Google Cloud, Azure, or Oracle
Cloud. I will be using Oracle Cloud for this guide as it provides a free tier that is sufficient for running the 
backend (at the cost of a performance hit when rendering 3D models). Please follow the following guides to set up an
Oracle Cloud instance (ensure that you create an Ubuntu 22.04 instance running with an x86 architecture):
1. [Oracle Cloud: Free Tier Account Sign-Up](https://oracle-base.com/articles/vm/oracle-cloud-free-tier-account-sign-up#next-steps)
2. [Oracle Cloud Infrastructure (OCI) : Create a Compartment](https://oracle-base.com/articles/vm/oracle-cloud-infrastructure-oci-create-a-compartment)
3. [Oracle Cloud Infrastructure (OCI) : Create a Virtual Cloud Network (VCN)](https://oracle-base.com/articles/vm/oracle-cloud-infrastructure-oci-create-a-virtual-cloud-network-vcn)
4. [Oracle Cloud Infrastructure (OCI) : Create a Compute VM](https://oracle-base.com/articles/vm/oracle-cloud-infrastructure-oci-create-a-compute-vm)

You will have to `SSH` into the server in order to access a terminal. The "Create a Compute VM" guide will show you how
to do this. However, if you will be connecting regularly, I suggest using a tool such as `Termius` which will allow you
to save the server's details and connect with a single click. You can download `Termius` from the following link:
[Termius](https://termius.com/).

### Installation of Required Software
To simplify the installation and configuration of the required software, we have created a script that will install all
the necessary software and configure the server environment. It can be run as follows from the root directory of the
repository:

```bash
./linux_server_install.sh
```
## Running the Backend
Once the installation script has been run, the backend is ready to be started. To start the backend, run the following
script from the root directory of the repository as follows:

```bash
./run_backend.sh
```
The backend will now be running on the server. If it shuts down or you would like to restart it, simply run the command 
again. however it will not be accessible from the internet. To make it accessible from the internet, you must follow
the networking instructions in the next section.

## Networking
### Server Firewall
In order to access the backend from the internet, the first step is to allow the backend port through the server's
firewall. The Aspenlog 2020 backend runs on port `42613` by default. To allow traffic through this port, run the
following commands:

```bash
sudo apt update
sudo apt -y install firewalld
sudo firewall-cmd --permanent --zone=public --add-port=42613/tcp
sudo firewall-cmd --reload
```

### Static IP Addresses
In your router settings, you must ensure that the server has a static IP address on your network. The instructions for
this are different for every router, so you will have to look up the instructions for your specific router. If you are
using Oracle Cloud, it has already been done for you. The IP address of your network must also be static. Again, if you
are using Oracle Cloud this has already been done for you. If you are not using a cloud service, and are using a 
residential internet connection, you can use a service such as `No-IP` to get a static IP address in the form of a 
DDNS. You can find more information on how to set up `No-IP` here: 
[No-IP Free Dynamic DNS](https://www.noip.com/remote-access).

### Domain
The next step is to run the backend over HTTPS. You may skip to the Port Forwarding section if you want to run the
backend over HTTP, however, it is **STRONGLY** encouraged to run the backend over HTTPS for security reasons. To do 
this, you must have a domain. If you do not have a domain, you can purchase one from a domain registrar. For this guide,
I will be using `CloudFlare` as we will need to use their services for the next step. More information on how to
purchase a domain from `CloudFlare` can be found here: 
[CloudFlare Domains](https://www.cloudflare.com/en-ca/products/registrar/). Once you have a domain, you must points its
A record to the static IP address of your network. You can find more information on how to do this here:
[CloudFlare DNS](https://support.cloudflare.com/hc/en-us/articles/360019093151-Managing-DNS-records-in-Cloudflare).

### SSL Certificate
The next step is to obtain an SSL certificate for your domain. This can be done for free using `Let's Encrypt`. To do
this, you must follow this guide: 
[Wildcard SSL Certificates with Certbot + Cloudflare](https://labzilla.io/blog/cloudflare-certbot). Once this is
complete, you must install HaProxy and configure it to use the SSL certificate. You can install HaProxy by running the
following command:

```bash
sudo apt -y install haproxy
```

Once HaProxy is installed, you must make your SSL certificate compatible with it. You can can do this by running the
following command (esuring to replace `<your-domain>` with your domain for example `aspenlog2020.com`):

```bash
cat "/etc/letsencrypt/live/<your-domain>/fullchain.pem" "/etc/letsencrypt/live/<your-domain>/privkey.pem" > "/etc/ssl/certs/<your-domain>.pem"
```

Now we must configure HaProxy to use the SSL certificate for the backend. You can do this by running the following
command:

```bash
sudo nano /etc/haproxy/haproxy.cfg
```

You must then add the following lines to the end of the file:

```bash
frontend aspenlog_frontend
        bind *:42613
        bind *:42613 ssl crt /etc/ssl/certs/<your-domain>.pem
        redirect scheme https code 301 if !{ ssl_fc }
        default_backend aspenlog_backend

backend aspenlog_backend
        server aspenlog_api 127.0.0.1:42613 check
```

Make sure to replace `<your-domain>` with your domain. Once this is done, you can press `Ctrl + X` to exit the file and
then press `Y` to save the changes. You can then restart HaProxy by running the following command:

```bash
sudo systemctl restart haproxy
```

### Port Forwarding
The final step is to allow traffic through the server's router. This is done by port forwarding. The instructions for
this are different for every router, so you will have to look up the instructions for your specific router. If you are
using Oracle Cloud, you can navigate to the `Default Security List` in the `Virtual Cloud Network` section of the
Oracle Cloud console and add an ingress rule to allow traffic through port `42613` shown in the following table:

| **Stateless** | **Source** | **IP Protocol** | **Source Port Range** | **Destination Port Range** | **Type and Code** |          **Allows**          |  **Description** |
|:-------------:|:----------:|:---------------:|:---------------------:|:--------------------------:|:-----------------:|:----------------------------:|:----------------:|
|       No      |  0.0.0.0/0 |       TCP       |          All          |            42613           |                   | TCP traffic for ports: 42613 | Aspenlog Backend |

### Testing the Network
Everything should now be set up and you should be able to access the backend from the internet. You can test this by
downloading the latest release of the frontend from the releases page and running it. You can then enter the domain of
in the `Connection Details` page and click `Connect`. If the frontend connects to the backend, everything is set up
correctly. If it does not connect, ensure that you have followed all the steps in this guide correctly.