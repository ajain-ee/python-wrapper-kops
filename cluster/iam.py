import boto3


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


