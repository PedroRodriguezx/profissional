import boto3

def copy_rds_parameter_group(source_region, source_parameter_group_name, destination_region, destination_parameter_group_name):
    # Create RDS clients for source and destination regions
    source_rds_client = boto3.client('rds', region_name=source_region)
    destination_rds_client = boto3.client('rds', region_name=destination_region)

    # Describe source parameter group
    source_parameter_group = source_rds_client.describe_db_parameter_groups(
        DBParameterGroupName=source_parameter_group_name
    )['DBParameterGroups'][0]

    # Create destination parameter group
    destination_rds_client.create_db_parameter_group(
        DBParameterGroupName=destination_parameter_group_name,
        DBParameterGroupFamily=source_parameter_group['DBParameterGroupFamily'],
        Description=source_parameter_group['Description']
    )

    # Copy parameters from source to destination parameter group
    for parameter in source_parameter_group['Parameters']:
        destination_rds_client.modify_db_parameter_group(
            DBParameterGroupName=destination_parameter_group_name,
            Parameters=[{
                'ParameterName': parameter['ParameterName'],
                'ParameterValue': parameter['ParameterValue'],
                'ApplyMethod': parameter['ApplyMethod']
            }]
        )

    print(f"Parameter group {destination_parameter_group_name} copied successfully.")

# Example usage
source_region = 'us-east-1'
source_parameter_group_name = 'source-parameter-group-name'
destination_region = 'us-west-2'
destination_parameter_group_name = 'destination-parameter-group-name'

copy_rds_parameter_group(source_region, source_parameter_group_name, destination_region, destination_parameter_group_name)
