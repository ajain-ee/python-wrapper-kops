import argparse
from subprocess import call
from typing import List

import boto3
import yaml
from jinja2 import Environment, PackageLoader, FileSystemLoader
import os


class AWSPolicy:
    effect: str
    action: List[str]
    resource: str = "*"

    def __init__(self, effect, action, resource):
        self.effect = effect
        self.action = action
        self.resource = resource


class KopsNodePolicies:
    policies: List[AWSPolicy] = []

    def __init__(self, policies: List):
        for _ in policies: self.policies.append(AWSPolicy(_.get('Effect'), _.get('Action'), _.get('Resource')))


class KopsMasterPolicies:
    policies: List[AWSPolicy] = []

    def __init__(self, policies):
        for _ in policies: self.policies.append(AWSPolicy(_.get('Effect'), _.get('Action'), _.get('Resource')))


class KopsClusterConfiguration():
    master_policies: KopsMasterPolicies
    node_policies: KopsNodePolicies

    def __init__(self, provider, cluster, additional_policies):
        self.cloud = provider
        self.cluster_name = cluster['name']
        self.vpc_id = cluster['vpc-id']
        self.bucket_name = cluster['s3-bucket']
        self.dns = cluster['dns']
        self.node_size = cluster['node-size']
        self.master_size = cluster['master-size']
        self.node_count = cluster['node-count']
        self.zones = cluster['zones']
        self.master_zones = cluster['master-zones']
        self.node_policies = KopsNodePolicies(additional_policies['node'])
        self.master_policies = KopsNodePolicies(additional_policies['master'])


class S3SUBNETCONFIG:
    cidr: str
    name: str
    type: str
    zone: str

    def __init__(self, cidr, name, type, zone):
        self.cidr = cidr
        self.name = name
        self.type = type
        self.zone = zone


def create_default_cluster(cluster_conf):
    stream = open(cluster_conf, 'r')

    cluster_config = yaml.safe_load(stream)

    kops_config = KopsClusterConfiguration(cluster_config.get('kops')['provider']['name'],
                                           cluster_config.get('kops')['provider']['cluster'],
                                           cluster_config.get('kops')['provider']['additionalPolicies']
                                           )

    stream.close()
    #
    # # print(kops_config.node_policies)
    # # create_s3_bucket(kops_config.bucket_name)
    #
    # f = open("s3_template.yaml", "w")
    #
    # call(['kops', 'create', 'cluster',
    #       '--name=' + kops_config.cluster_name,
    #       '--state=s3://' + kops_config.bucket_name,
    #       '--cloud=' + kops_config.cloud,
    #       '--node-size=' + kops_config.node_size,
    #       '--master-size=' + kops_config.master_size,
    #       '--node-count=2',
    #       '--master-count=3',
    #       '--zones=eu-central-1a,eu-central-1b,eu-central-1c',
    #       '--topology=private',
    #       '--networking=weave',
    #       '--dry-run',
    #       '-o', 'yaml',
    #       ], stdout=f)
    #
    # f.close()
    #
    # import ruamel.yaml
    #
    # yaml1 = ruamel.yaml.YAML()
    #
    # subnets: List[S3SUBNETCONFIG] = []
    # for idx, data in enumerate(yaml1.load_all(open('s3_template.yaml'))):
    #     if 0 == idx:
    #         subnets_dict = data["spec"]["subnets"]
    #         cluster_network_cidr = data["spec"]["networkCIDR"]
    #         for _ in subnets_dict:
    #             subnets.append(S3SUBNETCONFIG(_.get('cidr'), _.get('name'), _.get('type'), _.get('zone')))
    #
    #
    # kops_config
    #
    # #print(subnets[0]["name"])
    #
    # #s3_stream.close()
    #
    # # populate the template
    #
    # file_loader = FileSystemLoader('/Users/anuj/workspace/bcg/test-python-framework/templates')
    # env = Environment(loader=file_loader)
    #
    # cluster_template = env.get_template('multi-az-kops-template.yaml.j2')
    #
    #
    # root = os.path.dirname(os.path.abspath(__file__))
    #
    # filename = os.path.join(root, '', 'cluster.yaml')
    #
    # with open(filename, 'w') as fh:
    #     fh.write(cluster_template.render(
    #         cluster_name=kops_config.cluster_name,
    #         cluster_s3_bucket_name=kops_config.bucket_name,
    #         REGION="eu-central-1",
    #         subnets=subnets,
    #         cluster_network_cidr = cluster_network_cidr
    #     ))
    #
    # call(['kops', 'replace', '-f', 'cluster.yaml', '--state=s3://' + kops_config.bucket_name, '--force'])
    # call(['kops', 'create', 'secret', '--name', 'test-python-framework.k8s.local', 'sshpublickey', 'admin', '-i', '/Users/anuj/.ssh/id_rsa.pub', '--state=s3://' + kops_config.bucket_name])

    # call(['kops', 'create', 'cluster',
    #       '--name=' + kops_config.cluster_name,
    #       '--state=s3://' + kops_config.bucket_name,
    #       '--vpc=' + kops_config.vpc_id,
    #       '--network-cidr=192.168.246.0/24',
    #       '--dns=' + kops_config.dns,
    #       '--cloud=' + kops_config.cloud,
    #       '--node-size=' + kops_config.node_size,
    #       '--master-size=' + kops_config.master_size,
    #       '--zones=' + kops_config.zones,
    #       '--topology=private',
    #       '--networking=weave',
    #       '--yes'])

    # call(['kops', 'update', 'cluster',
    #       '--name=' + kops_config.cluster_name,
    #       '--state=s3://' + kops_config.bucket_name,
    #       '--yes'])

    delete_cluster(kops_config=kops_config)




def delete_cluster(kops_config):
    call(['kops', 'delete', 'cluster',
          '--name=' + kops_config.cluster_name,
          '--state=s3://' + kops_config.bucket_name,
          '--yes'])


def create_s3_bucket(bucket_name):
    client = boto3.client('s3')
    response = client.create_bucket(
        ACL='private',
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'EU'
        }

    )


# def update_cluster(cluster_conf):
#
#     client = boto3.client('s3')
#
#     client.get_object(Bucket="", key="")
#
#     stream = open(cluster_conf, 'r')
#
#     cluster_config = yaml.safe_load(stream)
#
#
#     kops_config = KopsClusterConfiguration(cluster_config.get('kops')['provider']['name'],
#                                            cluster_config.get('kops')['provider']['cluster'],
#                                            cluster_config.get('kops')['provider']['additionalPolicies']
#                                            )
#
#
#     # call(['kops', 'update', 'cluster',
#     #       '--name=' + kops_config.cluster_name,
#     #       '--state=s3://' + kops_config.bucket_name,
#     #       '--dns=' + kops_config.dns,
#     #       '--out=./terraform-git/' + kops_config.cluster_name,
#     #       '--target=terraform',
#     #       '--cloud=' + kops_config.cloud,
#     #       '--node-size=' + kops_config.node_size,
#     #       '--master-size=' + kops_config.master_size,
#     #       '--zones=' + kops_config.zones,
#     #       '--master_zones=' + kops_config.master_zones])

def setup_iam():
    print('Creating KOPS user and group on AWS')
    iam_client = boto3.client('iam')
    group_name = 'kops'
    user_name = 'kops'
    iam_policies = [
        'AmazonEC2FullAccess',
        'AmazonRoute53FullAccess',
        'AmazonS3FullAccess',
        'IAMFullAccess',
        'AmazonVPCFullAccess']

    try:
        iam_client.create_group(GroupName=group_name)
    except Exception as e:
        print(e)
        pass

    try:
        for policy in iam_policies:
            policy_string = 'arn:aws:iam::aws:policy/' + policy
            iam_client.attach_group_policy(GroupName=group_name, PolicyArn=policy_string)
    except Exception as e:
        print('ERROR: ' + str(e))
        pass

    try:
        iam_client.create_user(UserName=user_name)
    except Exception as e:
        print('ERROR: ' + str(e))
        pass

    try:
        iam_client.add_user_to_group(GroupName=group_name, UserName=user_name)
    except Exception as e:
        print('ERROR: ' + str(e))
        pass

    try:
        iam_client.create_access_key(UserName=user_name)
    except Exception as e:
        print('ERROR: ' + str(e))
        pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser()


    parser.add_argument("--config", help="Configuration file to provision k8 cluster", required=True)

    args = parser.parse_args()

    # setup_iam()

    create_default_cluster(args.config)




