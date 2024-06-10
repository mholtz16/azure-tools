from azure.identity import DefaultAzureCredential
import json
from account import Account
from ipaddress import ip_network,ip_address
import csv
ips=[]
with open ('ipam.csv','r') as csvfile:
    r = csv.reader(csvfile,delimiter=',')
    for row in r:
        ips.append(row[0].split('/',1)[0])

'''

with open('creds.json','r') as c:
    creds=json.loads(c.read())


azure_creds=creds['azure']
client = azure_creds['client']
tenant = azure_creds['tenant']
secret=azure_creds['secret']['value']
'''
credentials = DefaultAzureCredential()
ac = Account(credentials)

for sub in ac.subscriptions:
    for rg in sub.get_resource_groups():
        vnets = rg.network_client.virtual_networks.list(rg.name)
        for nic in sub.network_client.network_interfaces.list(rg.name):
            for ipc in nic.ip_configurations:
                if ipc.private_ip_address in ips:
                    print(f'found {nic.name} {ipc.private_ip_address} in ipam')
                else:
                    print(f'need to add {nic.name} {ipc.private_ip_address} to ipam')

#        for vn in vnets:
#            exit()
#            for sn in vn.subnets:
#                if sn.ip_configurations:
#                    for ipc in sn.ip_configurations:
#                        print(ipc.name,ipc.private_ip_address)
            # if it's not peered it doesn't really matter
            #if len(vn.virtual_network_peerings) > 0:  
            #    print(f'{rg.name} {vn.name} {vn.address_space.address_prefixes}')
            #network_interface_ip_configurations.list(rgname,nicname)



'''
['DEFAULT_API_VERSION', 'LATEST_PROFILE', '_PROFILE_TAG', '__abstractmethods__', '__annotations__', '__class__', '__delattr__', '__dict__', 
'__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__',
'__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
'__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__weakref__', '_abc_impl', '_api_version', '_client', '_config', 
'_delete_bastion_shareable_link_initial', '_deserialize', '_generatevirtualwanvpnserverconfigurationvpnprofile_initial',
'_get_active_sessions_initial', '_get_api_version', '_models_dict', '_put_bastion_shareable_link_initial', '_serialize',
'active_connectivity_configurations', 'active_security_admin_rules', 'active_security_user_rules', 'admin_rule_collections', 
'admin_rules', 'application_gateway_private_endpoint_connections', 'application_gateway_private_link_resources', 
'application_gateway_waf_dynamic_manifests', 'application_gateway_waf_dynamic_manifests_default', 'application_gateways',
'application_security_groups', 'available_delegations', 'available_endpoint_services', 'available_private_endpoint_types',
'available_resource_group_delegations', 'available_service_aliases', 'azure_firewall_fqdn_tags', 'azure_firewalls', 'bastion_hosts',
'begin_delete_bastion_shareable_link', 'begin_generatevirtualwanvpnserverconfigurationvpnprofile', 'begin_get_active_sessions', 
'begin_put_bastion_shareable_link', 'bgp_service_communities', 'check_dns_name_availability', 'close', 
'configuration_policy_groups', 'connection_monitors', 'connectivity_configurations', 'custom_ip_prefixes', 'ddos_custom_policies',
'ddos_protection_plans', 'default_security_rules', 'disconnect_active_sessions', 'dscp_configuration',
'effective_connectivity_configurations', 'effective_virtual_networks', 'express_route_circuit_authorizations', 
'express_route_circuit_connections', 'express_route_circuit_peerings', 'express_route_circuits', 'express_route_connections',
'express_route_cross_connection_peerings', 'express_route_cross_connections', 'express_route_gateways', 
'express_route_links', 'express_route_port_authorizations', 'express_route_ports', 'express_route_ports_locations', 
'express_route_provider_port', 'express_route_provider_ports_location', 'express_route_service_providers', 
'firewall_policies', 'firewall_policy_idps_signatures', 'firewall_policy_idps_signatures_filter_values', 
'firewall_policy_idps_signatures_overrides', 'firewall_policy_rule_collection_groups', 'firewall_policy_rule_groups', 
'flow_logs', 'get_bastion_shareable_link', 'hub_route_tables', 'hub_virtual_network_connections', 'inbound_nat_rules', 
'inbound_security_rule', 'interface_endpoints', 'ip_allocations', 'ip_groups', 'list_active_connectivity_configurations', 
'list_active_security_admin_rules', 'list_network_manager_effective_connectivity_configurations', 
'list_network_manager_effective_security_admin_rules', 'load_balancer_backend_address_pools', 'load_balancer_frontend_ip_configurations', 
'load_balancer_load_balancing_rules', 'load_balancer_network_interfaces', 'load_balancer_outbound_rules', 'load_balancer_probes', 
'load_balancers', 'local_network_gateways', 'management_group_network_manager_connections', 'nat_gateways', 'nat_rules', 'network_groups', 
'network_interface_ip_configurations', 'network_interface_load_balancers', 'network_interface_tap_configurations', 'network_interfaces', 
'network_manager_commits', 'network_manager_deployment_status', 'network_manager_effective_security_admin_rules', 'network_managers', 
'network_profiles', 'network_security_groups', 'network_security_perimeters', 'network_virtual_appliance_connections', 
'network_virtual_appliances', 'network_watchers', 'nsp_access_rules', 'nsp_access_rules_reconcile', 'nsp_association_reconcile', 
'nsp_associations', 'nsp_link_references', 'nsp_links', 'nsp_profiles', 'operations', 'p2_svpn_gateways', 'p2_svpn_server_configurations', 
'packet_captures', 'peer_express_route_circuit_connections', 'perimeter_associable_resource_types', 'private_dns_zone_groups', 
'private_endpoints', 'private_link_services', 'profile', 'public_ip_addresses', 'public_ip_prefixes', 'resource_navigation_links', 
'route_filter_rules', 'route_filters', 'route_maps', 'route_tables', 'routes', 'routing_intent', 'scope_connections', 
'security_admin_configurations', 'security_partner_providers', 'security_rules', 'security_user_configurations', 
'service_association_links', 'service_endpoint_policies', 'service_endpoint_policy_definitions', 'service_tag_information', 'service_tags', 
'static_members', 'subnets', 'subscription_network_manager_connections', 'supported_security_providers', 'usages', 'user_rule_collections', 
'user_rules', 'vip_swap', 'virtual_appliance_sites', 'virtual_appliance_skus', 'virtual_hub_bgp_connection', 'virtual_hub_bgp_connections', 
'virtual_hub_ip_configuration', 'virtual_hub_route_table_v2_s', 'virtual_hubs', 'virtual_network_gateway_connections', 
'virtual_network_gateway_nat_rules', 'virtual_network_gateways', 'virtual_network_peerings', 'virtual_network_taps', 'virtual_networks', 
'virtual_router_peerings', 'virtual_routers', 'virtual_wans', 'vpn_connections', 'vpn_gateways', 'vpn_link_connections', 
'vpn_server_configurations', 'vpn_server_configurations_associated_with_virtual_wan', 'vpn_site_link_connections', 'vpn_site_links', 
'vpn_sites', 'vpn_sites_configuration', 'web_application_firewall_policies', 'web_categories']



subnet:

 'additional_properties'
 'address_prefix'
 'address_prefixes'
 'application_gateway_ip_configurations'
 'as_dict'
 'default_outbound_access'
 'delegations'
 'deserialize'
 'enable_additional_properties_sending'
 'etag'
 'from_dict'
 'id'
 'ip_allocations'
 'ip_configuration_profiles'
 'ip_configurations'
 'is_xml_model'
 'name'
 'nat_gateway'
 'network_security_group'
 'private_endpoint_network_policies'
 'private_endpoints'
 'private_link_service_network_policies'
 'provisioning_state'
 'purpose'
 'resource_navigation_links'
 'route_table'
 'serialize'
 'service_association_links'
 'service_endpoint_policies'
 'service_endpoints'
 'type']


 '''