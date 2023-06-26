"""Python script to generate AWS config for aws-vault"""

import os
import sys
import configparser

config = configparser.ConfigParser()
config.read(os.path.expanduser("~/.aws/config"))
profile_names = config.sections()

list_of_roles = [
    {"role_name": "dev", "account_name": "tjth dev", "account_id": "000000000000", "region": "eu-west-2"},
    {"role_name": "dev", "account_name": "tjth prod", "account_id": "111111111111", "region": "eu-west-2"},
]

# Ask user for source profile name
source_profile = input("Enter source profile name: ")

if f"profile {source_profile}" not in profile_names:
    print(f"Source profile {source_profile} does not exist")
    print(f"Please add it to your aws-vault")
    sys.exit(1)

mfa_arn = config[f"profile {source_profile}"]["mfa_serial"]

for role in list_of_roles:
    profile_name = f'{role["role_name"]}_{role["account_name"]}'.lower().replace(" ", "_")
    print(profile_names)
    if f"profile {profile_name} " not in profile_names:
        print("Adding profile: ", profile_name)
        with open(os.path.expanduser(f"~/.aws/config"), "a") as config_file:
            config_file.write(
            '\n\n'
            f'[profile {profile_name} ]\n'
            f'region = {role["region"]}\n'
            f'source_profile = {source_profile}\n'
            f'role_arn = arn:aws:iam::{role["account_id"]}:role/{role["role_name"]}\n'
            f'mfa_serial = {mfa_arn}\n'
        )
    else:
        print(f"Profile {profile_name} already exists")
