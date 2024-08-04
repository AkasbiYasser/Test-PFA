variable "resource_group_name" {
    description = "The name of the resource group in which to create the cluster"
    default     = "Akasbiserver_group"
  }
  
  variable "location" {
    description = "The location of the resource group"
    default     = "South Africa North"
  }
  
  variable "aks_cluster_pfa" {
    description = "The name of the AKS cluster"
    default     = "aksClusterpfa"
  }
