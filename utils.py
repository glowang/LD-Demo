import ldclient
from ldclient.config import Config
from ldclient.integrations import Files
import os
from ldclient.config import Config
import argparse
from colorama import Fore

ld_client = None


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--flag", "-f", required=True, help="feature flag that you want to evaluate"
    )
    parser.add_argument(
        "--country", "-s", required=False, help="User's country attribute"
    )
    parser.add_argument("--key", "-k", required=False, help="User's identifying key")
    return parser


def get_command_args(parser):
    args = parser.parse_args()
    feature_flag = args.flag
    country = args.country
    user_key = args.key
    return feature_flag, country, user_key


def initialize_ld_client(read_from_file=False):
    # Initialize the ldclient with your environment-specific SDK key.
    # Doing so ensures that the SDK is used as a singleton
    if read_from_file:
        set_config_for_read_from_file()
    else:
        set_config_for_sdk_instance()
    global ld_client
    if ld_client is not None:
        return ld_client

    ld_client = ldclient.get()
    if ld_client.is_initialized():
        show_message("SDK successfully initialized!")
        return ld_client
    else:
        show_message("SDK failed to initialize")
        exit()

def set_config_for_read_from_file():
    data_source_callback = Files.new_data_source(paths=["flagdata.json"],
    auto_update=True)
    config = Config(os.getenv("LD_SDK_KEY"), update_processor_class=data_source_callback, send_events=False)
    ldclient.set_config(config) 

def set_config_for_sdk_instance():
    sdk_key = os.getenv("LD_SDK_KEY")
    if sdk_key is None:
        show_message("LaunchDarkly SDK Env Var LD_SDK_KEY is unset")
        exit()
    ldclient.set_config(Config(sdk_key))


def is_feature_flag_enabled(flag_name, user, default_value):
    detail = ld_client.variation_detail(key=flag_name, user=user, default=default_value)
    flag_value = detail.value
    reason = detail.reason["kind"]
    debug_info = detail.reason
    success_cases = ["RULE_MATCH", "TARGET_MATCH", "OFF"]
    if reason not in success_cases:
        display_message_for_error_cases(detail, flag_name)
        return {"value": flag_value}

    return {"value": flag_value, "reason": reason, "debug_info": debug_info}


def display_message_for_error_cases(detail, flag_name):
    failure_messages = {
        "ERROR": "Unexpected issue occur during the feature flag evaluation. Using default flag value.",
        "FALLTHROUGH": "The flag is on, but the user did not match any targets or rules,"
        "returning value under default rule",
        "PREREQUISITE_FAILED": "The flag had prerequisite flag that was off & returned undesired value",
    }
    reason = detail.reason["kind"]
    message = failure_messages[reason]
    debug_info = {"feature_flag": flag_name}
    show_message(f"{message}, debug info: {debug_info}")


def get_launchdarkly_user(country: str, key: str):
    ld_user = {}

    if key is None:
        show_message(Fore.RED + "Parameter --key is unset, using default key default_user")
        key = "default_user"
    ld_user["key"] = key
    if country is not None:
        ld_user["country"] = country
    return ld_user


def display_flag_result(results, feature_flag):
    flag_value = results["value"]
    reason = results.get("reason")
    debug_info = results.get("debug_info")
    print(
        Fore.GREEN + f"Feature flag {feature_flag} is {flag_value} for this user. Reason: {reason}. Debug: {debug_info}"
    )


def show_message(s):
    print("*** %s" % s)
    print()
