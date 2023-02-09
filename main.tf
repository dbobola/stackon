provider "azurerm" {
  version = "2.0"
  features {}
}

locals {
  version = "1.25.5"
}

data "azurerm_client_config" "current" {
}

variable "ARM_CLIENT_SECRET" {
  description = "The client secret for authentication with Azure"
  default = "$ARM_CLIENT_SECRET"
}
variable "ARM_CLIENT_ID" {
  description = "The client secret for authentication with Azure"
  default = "$ARM_CLIENT_ID"
}
variable "region" {
  type = string
  default = "UAE North"
}

variable "aks_cluster_name" {
  type = string
  default = "stackonaks"
}

variable "acr_name" {
  type = string
  default = "stackonacr"
}

variable "sql_server_name" {
  type = string
  default = "stackonsvr"
}

variable "sql_db_name" {
  type = string
  default = "stackondb"
}

variable "stg_acc_name" {
  type = string
  default = "stackonstorageaccount"
}

variable "stg_con_name" {
  type = string
  default = "stackonstoragecontainer"
}


resource "azurerm_resource_group" "stackonrg" {
  name     = "stackonrg"
  location = var.region
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.aks_cluster_name
  location            = azurerm_resource_group.stackonrg.location
  resource_group_name = azurerm_resource_group.stackonrg.name
  kubernetes_version  = local.version
  dns_prefix          = "my-aks"

  linux_profile {
    admin_username = "azureuser"

    ssh_key {
      key_data = file("~/.ssh/id_rsa.pub")
    }
  }

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_DS2_v2"
  }

  service_principal {
     client_id = "${var.ARM_CLIENT_ID}"
     client_secret = "${var.ARM_CLIENT_SECRET}"
   }

  role_based_access_control {
    enabled = false
  }
}

resource "azurerm_container_registry" "acr" {
  name                  = var.acr_name
  resource_group_name   = azurerm_resource_group.stackonrg.name
  location              = azurerm_resource_group.stackonrg.location
  sku                   = "Standard"
  admin_enabled         = false
 
}

# resource "azurerm_kubernetes_cluster_container_registry_association" "association" {
#   cluster_name      = azurerm_kubernetes_cluster.aks.name
#   resource_group_name = azurerm_resource_group.stackonrg.name
#   registry_id       = azurerm_container_registry.acr.id
# }

resource "azurerm_sql_server" "sql_server" {
  name                         = var.sql_server_name
  resource_group_name          = azurerm_resource_group.stackonrg.name
  location                     = azurerm_resource_group.stackonrg.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P2ssw0rd1234"
}

resource "azurerm_sql_database" "sql_database" {
  name                             = var.sql_db_name
  resource_group_name             = azurerm_resource_group.stackonrg.name
  location                     = azurerm_resource_group.stackonrg.location
  server_name                      = azurerm_sql_server.sql_server.name
  create_mode                      = "Default"
  requested_service_objective_name = "S0"
}

resource "azurerm_storage_account" "storageaccount" {
  name                     = var.stg_acc_name
  resource_group_name     = azurerm_resource_group.stackonrg.name
  location                 = azurerm_resource_group.stackonrg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "storage-container" {
  name                  = var.stg_con_name
  storage_account_name = azurerm_storage_account.storageaccount.name
  container_access_type = "private"
}

terraform {
  backend "azurerm" {
    resource_group_name =  "one2oneapi"
    storage_account_name = "one2onestorageaccount"
    container_name = "one2oneblobcontainer"
    key                  = "terraform.tfstate"
  }
}