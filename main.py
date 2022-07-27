from utils import (
    initialize_ld_client,
    get_launchdarkly_user,
    is_feature_flag_enabled,
    create_parser,
    get_command_args,
    display_flag_result,
)


def evaluate_feature_flag_value():
    """
    This function 1) takes arguments from the command line, 2) initiates an
    instance of the LD SDK client, 3) evaluates the feature flag, and 4)
    displays the value back.
    """
    parser = create_parser()
    feature_flag, country, user_key = get_command_args(parser)
    ld_client = initialize_ld_client()
    user = get_launchdarkly_user(country=country, key=user_key)
    results = is_feature_flag_enabled(feature_flag, user, False)
    display_flag_result(results, feature_flag)
    ld_client.close()


evaluate_feature_flag_value()
