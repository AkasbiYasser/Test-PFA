provider "azurerm" {
    features {}
  }
  
  resource "azurerm_resource_group" "aks_rg" {
    name     = "Akasbiserver_group"
    location = "South Africa North"
  }
  
  resource "azurerm_kubernetes_cluster" "aks" {
    name                = "aksCluster"
    location            = azurerm_resource_group.aks_rg.location
    resource_group_name = azurerm_resource_group.aks_rg.name
    dns_prefix          = "aks"
  
    default_node_pool {
      name       = "default"
      node_count = 1
      vm_size    = "Standard_DS2_v2"
    }
  
    identity {
      type = "SystemAssigned"
    }
  }
  
  output "kube_config" {
    value = azurerm_kubernetes_cluster.aks.kube_config_raw
  }
