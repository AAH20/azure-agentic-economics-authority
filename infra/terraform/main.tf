terraform {
  required_version = ">= 1.6"
  required_providers { azurerm = { source = "hashicorp/azurerm", version = "~> 4.0" } }
}
provider "azurerm" { features {} }
variable "location" { type = string, default = "eastus" }
variable "resource_group_name" { type = string, default = "rg-agentic-economics" }
resource "azurerm_resource_group" "this" { name = var.resource_group_name, location = var.location }
resource "azurerm_log_analytics_workspace" "this" { name = "law-agentic-economics", location = azurerm_resource_group.this.location, resource_group_name = azurerm_resource_group.this.name, retention_in_days = 30, sku = "PerGB2018" }
resource "azurerm_application_insights" "this" { name = "appi-agentic-economics", location = azurerm_resource_group.this.location, resource_group_name = azurerm_resource_group.this.name, application_type = "web", workspace_id = azurerm_log_analytics_workspace.this.id }

