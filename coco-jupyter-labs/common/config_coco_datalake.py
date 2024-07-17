#!/usr/bin/env python3
"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.



Egeria Coco Pharmaceutical demonstration labs.

This script configures and initiates the Egeria OMAG Servers deployed on the Datalake Platform.
It is automatically run whenever the Coco Lab Compose script is started.

"""

import argparse

from pyegeria import CoreServerConfig, Platform, FullServerConfig, ServerOps, print_exception_response


from globals import (corePlatformURL, cocoCohort, max_paging_size, cocoMDS1Name,
                     cocoMDS4Name, dataLakePlatformURL, fileSystemRoot, adminUserId)
class ConfigCocoDatalake(ServerOps):
    disable_ssl_warnings = True
    event_bus_config = {
        "producer": {
            "bootstrap.servers": "host.docker.internal:9192"
        },
        "consumer": {
            "bootstrap.servers": "host.docker.internal:9192"
        }
    }

    security_connection_body = {
        "class": "Connection",
        "connectorType": {
            "class": "ConnectorType",
            "connectorProviderClassName":
                "org.odpi.openmetadata.metadatasecurity.samples.CocoPharmaServerSecurityProvider"
        }
    }

    def __init__(self, server: str, url: str, admin_user: str):
        self.platform_url = url
        self.admin_user = admin_user
        Platform.__init__(self, server, url, admin_user)
        print("Configuring and starting the Data Lake")



    #
    # Configure MDS1
    #
    def config_mds1(self)-> None:
        mdr_server = cocoMDS1Name
        mdr_server_user_id = "cocoMDS1npa"
        mdr_server_password = "cocoMDS1passw0rd"
        metadataCollectionId = f"{mdr_server}-e915f2fa-aa3g-4396-8bde-bcd65e642b1d"
        metadataCollectionName = "Data Lake Operations"
    
        print("Configuring " + mdr_server + "...")
        try:
            o_client = CoreServerConfig(mdr_server, self.platform_url, self.admin_user)
    
            o_client.set_basic_server_properties(metadataCollectionName,
                                                 "Coco Pharmaceuticals",
                                                 self.platform_url,
                                                 mdr_server_user_id, mdr_server_password,
                                                 max_paging_size)
    
            o_client.set_event_bus(self.event_bus_config)
            o_client.set_server_security_connection(self.security_connection_body)
            o_client.add_default_log_destinations()
    
            # o_client.set_in_mem_local_repository()
            o_client.set_xtdb_local_kv_repository()
    
            o_client.set_local_metadata_collection_id(metadataCollectionId)
            o_client.set_local_metadata_collection_name(metadataCollectionName)
    
            o_client.add_cohort_registration(cocoCohort)
            access_service_options = {
                "SupportedZones": ["quarantine", "clinical-trials", "research", "data-lake", "trash-can"]
            }
    
            # o_client.configure_access_service("asset-catalog", {})
            o_client.configure_access_service("asset-consumer", {})
    
            access_service_options["DefaultZones"] = ["quarantine"]
            access_service_options["PublishZones"] = ["data-lake"]
    
            # print(f"Access Service Options: {access_service_options}")
    
            o_client.configure_access_service("asset-manager", access_service_options)
            o_client.configure_access_service("asset-owner", access_service_options)
            o_client.configure_access_service("community-profile",
                                              {"KarmaPointPlateau": "500"})
            # o_client.configure_access_service("glossary-view", {})
            # o_client.configure_access_service("data-engine", access_service_options)
            o_client.configure_access_service("data-manager", access_service_options)
            o_client.configure_access_service("digital-architecture", access_service_options)
            o_client.configure_access_service("governance-engine", access_service_options)
            o_client.configure_access_service("governance-server", access_service_options)
            o_client.configure_access_service("asset-lineage", access_service_options)

            print("Configuring Core Content Pack Archive for startup")
            o_client.add_startup_open_metadata_archive_file("content-packs/CoreContentPack.omarchive")

            print(f"Activating {mdr_server}")

            self.activate_server_stored_config(cocoMDS1Name)
            print(mdr_server + " activated")
    
        except Exception as e:
            print_exception_response(e)
    
    #
    # Configure MDS4
    #
    def config_mds4(self)->None:
        mdr_server = cocoMDS4Name
        mdr_server_user_id = "cocoMDS4npa"
        mdr_server_password = "cocoMDS4passw0rd"
        metadataCollectionId = f"{mdr_server}-e915f2fa-aa3g-4396-8bde-bcd65e642b1d"
        metadataCollectionName = "Data Lake Users"
        print("Configuring " + mdr_server + "...")
    
        try:
    
            o_client = CoreServerConfig(mdr_server, self.platform_url, self.admin_user)
    
            o_client.set_basic_server_properties("Data Lake Users",
                                                 "Coco Pharmaceuticals",
                                                 self.platform_url,
                                                 mdr_server_user_id, mdr_server_password,
                                                 max_paging_size)
    
    
            o_client.set_event_bus(self.event_bus_config)
            o_client.set_server_security_connection(self.security_connection_body)
            o_client.add_default_log_destinations()
    
            # Note: no metadata repository or collection configuration in this server.
    
            o_client.add_cohort_registration(cocoCohort)
    
            accessServiceOptions = {
                "SupportedZones": ["data-lake"]
            }
    
            # o_client.configure_access_service("asset-catalog", accessServiceOptions)
            o_client.configure_access_service("asset-consumer", accessServiceOptions)
            o_client.configure_access_service("asset-owner", {})
            o_client.configure_access_service("community-profile",
                                              {"KarmaPointPlateau": "500"})
            # o_client.configure_access_service("glossary-view", {})
            o_client.configure_access_service("data-science", accessServiceOptions)

            print(f"Activating {mdr_server}")

            self.activate_server_stored_config(cocoMDS4Name)
    
            print(f"{mdr_server} activated")
    
        except Exception as e:
            print_exception_response(e)
    
    #
    # Configure exchangeDL01
    #
    def config_exchangeDL01(self)-> None:
        daemon_server_name = "exchangeDL01"
        daemon_server_platform = self.platform_url
        daemon_server_user_id = "exchangeDL01npa"
        daemon_server_password = "exchangeDL01passw0rd"
    
        mdr_server = "cocoMDS1"
        folder_connector_name = "DropFootClinicalTrialResultsFolderMonitor"
        folder_connector_user_id = "monitorDL01npa"
        folder_connector_source_name = "DropFootClinicalTrialResults"
        folder_connector_folder = fileSystemRoot + '/data-lake/research/clinical-trials/drop-foot/weekly-measurements'
        folder_connector_connection = {
            "class": "Connection",
            "connectorType":
                {
                    "class": "ConnectorType",
                    "connectorProviderClassName":
                        "org.odpi.openmetadata.adapters.connectors.integration.basicfiles.DataFolderMonitorIntegrationProvider"
                },
            "endpoint":
                {
                    "class": "Endpoint",
                    "address": folder_connector_folder
                }
        }
    
        integration_group_name = "Onboarding"
    
        print("Configuring " + daemon_server_name)
    
        try:
            f_client = FullServerConfig(daemon_server_name, daemon_server_platform, self.admin_user)
    
            f_client.set_basic_server_properties("Supports exchange of metadata with third party technologies",
                                                 "Coco Pharmaceuticals",
                                                 daemon_server_platform,
                                                 daemon_server_user_id, daemon_server_password,
                                                 max_paging_size)
    
            f_client.set_server_security_connection(self.security_connection_body)
            f_client.add_default_log_destinations()
    
            connector_configs = [
                {
                    "class": "IntegrationConnectorConfig",
                    "connectorName": folder_connector_name,
                    "connectorUserId": folder_connector_user_id,
                    "connection": folder_connector_connection,
                    "metadataSourceQualifiedName": folder_connector_source_name,
                    "refreshTimeInterval": 10,
                    "usesBlockingCalls": "false"
                }
            ]
    
            f_client.config_integration_service(mdr_server, self.platform_url, "files-integrator",
                                                {}, connector_configs)
    
            f_client.config_integration_group(mdr_server, daemon_server_platform,
                                              integration_group_name)
            print(f"Activating {daemon_server_name}")

            self.activate_server_stored_config(daemon_server_name)
    
            print(f"{daemon_server_name} activated")
    
        except Exception as e:
            print_exception_response(e)
    
    #
    # Configure governDL01
    #
    def config_governDL01(self)->None:
        engine_server = "governDL01"
        engine_server_platform = self.platform_url
    
        engine_server_user_id = "governDL01npa"
        engine_server_password = "governDL01passw0rd"
        mdr_server = "cocoMDS1"
        mdr_engine_server_platform = dataLakePlatformURL
    
        print("Configuring " + engine_server)
    
        try:
            o_client = CoreServerConfig(engine_server, engine_server_platform, self.admin_user)
    
            o_client.set_basic_server_properties("An Engine Host to run governance actions for Coco Pharmaceuticals",
                                                 "Coco Pharmaceuticals",
                                                 engine_server_platform,
                                                 engine_server_user_id, engine_server_password,
                                                 max_paging_size)
    
            o_client.set_server_security_connection(self.security_connection_body)
    
            o_client.set_engine_definitions_client_config(mdr_server, mdr_engine_server_platform)
    
            engine_list_body = [
                {
                    "class": "EngineConfig",
                    "engineQualifiedName": "AssetDiscovery",
                    "engineUserId": "findItDL01npa"
                },
                {
                    "class": "EngineConfig",
                    "engineQualifiedName": "AssetQuality",
                    "engineUserId": "findItDL01npa"
                }
            ]
    
            o_client.set_engine_list(engine_list_body)
    
            # config = o_client.get_stored_configuration()
            # print(f"The server stored configuration is {json.dumps(config, indent=4)}")
            print(f"Activating {engine_server}")
            self.activate_server_stored_config(engine_server)
            print(f"{engine_server} activated")
        except Exception as e:
            print_exception_response(e)

    #
    # Configure monitorGov1
    #
    def config_monitorGov01(self) -> None:
        daemon_server_name = "monitorGov01"
        daemon_server_platform = dataLakePlatformURL
        daemon_server_user_id = "exchangeDL01npa"
        daemon_server_password = "exchangeDL01passw0rd"

        mdr_server = "cocoMDS1"
        mdr_platform_url = dataLakePlatformURL
        admin_user = "garygeeke"

        KafkaReceiverConnectorName = "KafkaOpenLineageEventReceiver"
        KafkaReceiverConnectorUserId = "onboardDL01npa"
        KafkaReceiverConnectorSourceName = "Apache Kafka"
        KafkaReceiverConnectorConnection = {
            "class": "VirtualConnection",
            "connectorType":
                {
                    "class": "ConnectorType",
                    "connectorProviderClassName": "org.odpi.openmetadata.adapters.connectors.integration.openlineage.OpenLineageEventReceiverIntegrationProvider"
                },
            "embeddedConnections":
                [
                    {
                        "class": "EmbeddedConnection",
                        "embeddedConnection":
                            {
                                "class": "Connection",
                                "connectorType":
                                    {
                                        "class": "ConnectorType",
                                        "connectorProviderClassName": "org.odpi.openmetadata.adapters.eventbus.topic.kafka.KafkaOpenMetadataTopicProvider",
                                    },
                                "endpoint":
                                    {
                                        "class": "Endpoint",
                                        "address": "openlineage.topic"
                                    },
                                "configurationProperties":
                                    {
                                        "producer":
                                            {
                                                "bootstrap.servers": "host.docker.internal:9192"
                                            },
                                        "local.server.id": "f234e808-2d0c-4d88-83df-275eee20c1b7",
                                        "consumer":
                                            {
                                                "bootstrap.servers": "host.docker.internal:9192"
                                            }
                                    }
                            }
                    }
                ]
        }

        GovernanceActionConnectorName = "GovernanceActionOpenLineageCreator"
        GovernanceActionConnectorUserId = "onboardDL01npa"
        GovernanceActionConnectorSourceName = "Egeria"
        GovernanceActionConnectorConnection = {
            "class": "Connection",
            "connectorType":
                {
                    "class": "ConnectorType",
                    "connectorProviderClassName": "org.odpi.openmetadata.adapters.connectors.integration.openlineage.GovernanceActionOpenLineageIntegrationProvider"
                },
        }

        APILoggerConnectorName = "APIBasedOpenLineageLogStore"
        APILoggerConnectorUserId = "onboardDL01npa"
        APILoggerConnectorSourceName = "Egeria"
        APILoggerConnectorConnection = {
            "class": "Connection",
            "connectorType":
                {
                    "class": "ConnectorType",
                    "connectorProviderClassName": "org.odpi.openmetadata.adapters.connectors.integration.openlineage.APIBasedOpenLineageLogStoreProvider"
                },
            "endpoint":
                {
                    "class": "Endpoint",
                    "address": "http://host.docker.internal:5000/api/v1/lineage"
                }
        }

        FileLoggerConnectorName = "FileBasedOpenLineageLogStore"
        FileLoggerConnectorUserId = "onboardDL01npa"
        FileLoggerConnectorSourceName = "Egeria"
        FileLoggerConnectorConnection = {
            "class": "Connection",
            "connectorType":
                {
                    "class": "ConnectorType",
                    "connectorProviderClassName": "org.odpi.openmetadata.adapters.connectors.integration.openlineage.FileBasedOpenLineageLogStoreProvider"
                },
            "endpoint":
                {
                    "class": "Endpoint",
                    "address": fileSystemRoot + '/openlineage.log'
                }
        }

        CataloguerConnectorName = "OpenLineageCataloguer"
        CataloguerConnectorUserId = "onboardDL01npa"
        CataloguerConnectorSourceName = "OpenLineageSources"
        CataloguerConnectorConnection = {
            "class": "Connection",
            "connectorType":
                {
                    "class": "ConnectorType",
                    "connectorProviderClassName": "org.odpi.openmetadata.adapters.connectors.integration.openlineage.OpenLineageCataloguerIntegrationProvider"
                }
        }

        print("Configuring " + daemon_server_name + "...")

        connectorConfigs = [
            {
                "class": "IntegrationConnectorConfig",
                "connectorName": KafkaReceiverConnectorName,
                "connectorUserId": KafkaReceiverConnectorUserId,
                "connection": KafkaReceiverConnectorConnection,
                "metadataSourceQualifiedName": KafkaReceiverConnectorSourceName,
                "refreshTimeInterval": 10,
                "usesBlockingCalls": "false"
            },
            {
                "class": "IntegrationConnectorConfig",
                "connectorName": GovernanceActionConnectorName,
                "connectorUserId": GovernanceActionConnectorUserId,
                "connection": GovernanceActionConnectorConnection,
                "metadataSourceQualifiedName": GovernanceActionConnectorSourceName,
                "refreshTimeInterval": 10,
                "usesBlockingCalls": "false"
            },
            {
                "class": "IntegrationConnectorConfig",
                "connectorName": APILoggerConnectorName,
                "connectorUserId": APILoggerConnectorUserId,
                "connection": APILoggerConnectorConnection,
                "metadataSourceQualifiedName": APILoggerConnectorSourceName,
                "refreshTimeInterval": 10,
                "usesBlockingCalls": "false"
            },
            {
                "class": "IntegrationConnectorConfig",
                "connectorName": FileLoggerConnectorName,
                "connectorUserId": FileLoggerConnectorUserId,
                "connection": FileLoggerConnectorConnection,
                "metadataSourceQualifiedName": FileLoggerConnectorSourceName,
                "refreshTimeInterval": 10,
                "usesBlockingCalls": "false"
            },
            {
                "class": "IntegrationConnectorConfig",
                "connectorName": CataloguerConnectorName,
                "connectorUserId": CataloguerConnectorUserId,
                "connection": CataloguerConnectorConnection,
                "metadataSourceQualifiedName": CataloguerConnectorSourceName,
                "refreshTimeInterval": 10,
                "usesBlockingCalls": "false"
            }]

        try:
            f_client = FullServerConfig(daemon_server_name, dataLakePlatformURL, admin_user)

            f_client.set_basic_server_properties("An integration daemon server supporting the governance team",
                                                 "Coco Pharmaceuticals",
                                                 dataLakePlatformURL,
                                                 daemon_server_user_id, daemon_server_password,
                                                 max_paging_size)

            f_client.set_server_security_connection(self.security_connection_body)
            f_client.add_default_log_destinations()

            f_client.config_integration_service(mdr_server, mdr_platform_url,
                                                "lineage-integrator", {}, connectorConfigs)

            self.activate_server_stored_config(daemon_server_name)
            print("monitorGov01 has been activated")

        except Exception as e:
            print_exception_response(e)

    #
    # Configure cocoView1
    #
    def config_cocoView1(self) -> None:
        view_server = "cocoView1"
        view_server_user_id = "cocoView1npa"
        view_server_password = "cocoView1passw0rd"
        view_server_type = "View Server"
        remote_platform_url = corePlatformURL
        remote_server_name = cocoMDS1Name
    
        print("Configuring " + view_server)
        try:
            f_client = FullServerConfig(view_server, self.platform_url, self.admin_user)
    
            f_client.set_server_user_id(view_server_user_id)
            f_client.set_server_user_password(view_server_password)
            f_client.set_organization_name("Coco Pharmaceuticals")
    
            f_client.set_server_description("Coco View Server")
            f_client.set_server_url_root(self.platform_url)
            f_client.set_event_bus(self.event_bus_config)
            f_client.set_server_security_connection(self.security_connection_body)
    
            f_client.add_default_log_destinations()
    
            f_client.config_all_view_services(remote_server_name, self.platform_url)
            print(f"Activating {view_server}")
            self.activate_server_stored_config(view_server)
    
            print(f"{view_server} activated")
    
        except Exception as e:
            print_exception_response(e)
    
    #
    # Configure cocoOLS1
    #
    def config_cocoOLS1(self)->None:
        lineageServerName = "cocoOLS1"
        lineageServerPlatform = dataLakePlatformURL
    
        mdrServerName = "cocoMDS1"
        mdrServerUserId = "cocoMDS1npa"
        mdrServerPassword = "secret"
        mdrServerPlatform = dataLakePlatformURL
    
        print("Configuring " + lineageServerName)
    
        requestBody = {
            "class": "OpenLineageConfig",
            "openLineageDescription": "Open Lineage Service is used for the storage and querying of lineage",
            "lineageGraphConnection": {
                "class": "Connection",
                "displayName": "Lineage Graph Connection",
                "description": "Used for storing lineage in the Open Metadata format",
                "connectorType": {
                    "class": "ConnectorType",
                    "connectorProviderClassName": "org.odpi.openmetadata.openconnectors.governancedaemonconnectors.lineagewarehouseconnectors.janusconnector.graph.LineageGraphConnectorProvider"
                },
                "configurationProperties": {
                    "gremlin.graph": "org.janusgraph.core.JanusGraphFactory",
                    "storage.backend": "berkeleyje",
                    "storage.directory": "data/servers/" + lineageServerName + "/lineage-repository/berkeley",
                    "index.search.backend": "lucene",
                    "index.search.directory": "data/servers/" + lineageServerName + "/lineage-repository/searchindex"
                }
            },
            "accessServiceConfig": {
                "serverName": mdrServerName,
                "serverPlatformUrlRoot": mdrServerPlatform,
                "user": mdrServerUserId,
                "password": mdrServerPassword
            },
            "backgroundJobs": [
                {
                    "jobName": "LineageGraphJob",
                    "jobInterval": 120,
                    "jobEnabled": "false"
                },
                {
                    "jobName": "AssetLineageUpdateJob",
                    "jobInterval": 120,
                    "jobEnabled": "false",
                    "jobDefaultValue": "2021-12-03T10:15:30"
                }
            ]
        }
    
    
        try:
            f_client = FullServerConfig(lineageServerName, lineageServerPlatform, self.admin_user)
    
            f_client.set_server_description("Open Lineage Server")
            f_client.set_server_url_root(lineageServerPlatform)
            f_client.set_event_bus(self.event_bus_config)
            f_client.add_default_log_destinations()
    
            f_client.set_lineage_warehouse_services(requestBody, lineageServerName)
            print(f"Activating {lineageServerName}")
            self.activate_server_stored_config(lineageServerName)
    
            print(f"{lineageServerName} activated")
    
        except Exception as e:
            print_exception_response(e)

def main():
    print("\nStarting Datalake\n")
    parser = argparse.ArgumentParser()

    parser.add_argument("--url", help="URL Platform to connect to")
    parser.add_argument("--userid", help="User Id")
    args = parser.parse_args()

    url = args.url if args.url is not None else dataLakePlatformURL
    userid = args.userid if args.userid is not None else adminUserId

    try:
        client = ConfigCocoDatalake("cocoMDS1", url, userid)
        # Test if each server is known, and if run "activate_server_if_down", if not run the appropriate function
        if client.is_server_configured("cocoMDS1"):
            client.activate_server_if_down("cocoMDS1")
            print("cocoMDS1 is configured and is being activated")
        else:
            client.config_mds1()
            print("\n==>cocoMDS1 is being configured and activated")

        if client.is_server_configured("cocoMDS4"):
            client.activate_server_if_down("cocoMDS4")
            print("cocoMDS4 is configured and is being activated")
        else:
            client.config_mds4()
            print("\n==>cocoMDS4 is being configured and activated")

        if client.is_server_configured("exchangeDL01"):
            client.activate_server_if_down("exchangeDL01")
            print("exchangeDL01 is configured and is being activated")
        else:
            client.config_exchangeDL01()
            print("\n==>exchangeDL01 is being configured and activated")

        if client.is_server_configured("governDL01"):
            client.activate_server_if_down("governDL01")
            print("governDL01 is configured and is being activated")
        else:
            client.config_governDL01()
            print("\n==>governDL01 is being configured and activated")

        if client.is_server_configured("cocoView1"):
            client.activate_server_if_down("cocoView1")
            print("cocoView1 is configured and is being activated\n")
        else:
            client.config_cocoView1()
            print("\n==>cocoView1 is being configured and activated")

        if client.is_server_configured("cocoOLS1"):
            print("cocoOLS1 is configured and is being activated")
            client.activate_server_if_down("cocoOLS1")
        else:
            client.config_cocoOLS1()
            print("\n==>cocoOLS1 is being configured and activated")

        if client.is_server_configured("monitorGov01"):
            print("monitorGov01 is configured and is being activated")
            client.activate_server_if_down("monitorGov01")
        else:
            client.config_monitorGov01()
            print("\n==>monitorGov01 is being configured and activated")



    except Exception as e:
        print_exception_response(e)



if __name__ == "__main__":
    main()
