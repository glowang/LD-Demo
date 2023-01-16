# LaunchDarkly Sample Demo CLI tool (Python)

This CLI tool evaluates whether a specific feature flag is toggled on based on attributes 
such as country and user key.

## Requirements

Python version 3.5 or higher.


## Setup Instructions
1. Clone the repo at 
    ```bash
    https://github.com/glowang/LD-Demo.git
    ```
1. Install the LaunchDarkly Python SDK by running 
    ```
    cd ld-demo
    pip install -r requirements.txt`
    ```
    Note: if your system's default Python is Python2, you might need to run    
    ```
    cd ld-demo
    pip3 install -r requirements.txt
    ```

2. Set your environment variable `LD_SDK_KEY` to be the value of your LaunchDarkly SDK key. 
    - To find your SDK key, go to this page:
    https://docs.launchdarkly.com/sdk/concepts/client-side-server-side#keys
    - To set your environment vairable on the command line: 
        ```bash
        $ export LD_SDK_KEY=<sdk-my-secret-key>
        ```


## Testing out LaunchDarkly with Real Examples

### Use case 1: only show a feature to targeted users:
-  Create a new feature flag with the human readable name: `Show Feature to Target Users Only`. 
    The flag value will be autogenerated to be `show-feature-to-target-users-only`
-  Under `Individual Targeting` section, configure the flag to return `True` for user with key `select-user` 
-  Set the Default Rule to be returning `False`
-  If he flag is turned off, set the return value to `False` as well. 

### Playing with the first feature flag: `show-feature-to-target-users-only`
   - Scenario 1: a user with key `not-a-select-user` should get a `False` value for this feature flag. 
      Let's do it with the following command: 
        ```
        python3 main.py --flag "show-feature-to-target-users-only" --key "not-a-select-user" 
        ```
      - Since our user key is not being targeted, we received `False` as a result: 
        ```bash
        *** SDK successfully initialized!
        *** The flag is on, but the user did not match any targets or rules,returning value under default rule, debug info: {'feature_flag': 'show-feature-to-target-users-only'}
        *** Feature flag show-feature-to-target-users-only is False for this user. Reason: None. Debug: None
        ```
- Scenario 2: a user with key `select-user` should get a `True` value for this feature flag. 
      Let's do it with the following command: 
    ```bash
    $ python3 main.py --flag "show-feature-to-target-users-only" --key "select-user" 
    ```
    - As a expected, we would get:
        ```bash
        *** SDK successfully initialized!
        *** Feature flag show-feature-to-target-users-only is True for this user. Reason: TARGET_MATCH. Debug: {'kind': 'TARGET_MATCH'}
        ``` 

### User case 2: return different flag values based on user attribute (eg. country)
  - Create a flag named `provide-discount-to-us-users`
    -  create a new feature flag with the human readable name: `Provide Discount to US Users` 
    -  Under the section `Target users who match these rules`, configure the flag to return `80` for user with the "country" attribute containing `United States` 
    -  Set the Default Rule to return `100`
    - If the feature flag is turned off, we also want the price to be 100 to all users. Therefore, if targeting is off, we will serve `100`. 

### Experimenting with our second feature flag: `show-feature-to-us-users`:
- Scenario 1: evaluating the flag for US users:
    - Let's do it with the following command: 
        ```bash
        python3 main.py --flag "provide-discount-to-us-users" --country "United States"        
        ```
    - As a expected, we would get:
        ```bash
            
        *** SDK successfully initialized!

        *** Parameter --key is unset, using default key default_user

        *** Feature flag provide-discount-to-us-users is 80 for this user. Reason: RULE_MATCH. Debug: {'kind': 'RULE_MATCH', 'ruleIndex': 0, 'ruleId': '5f887263-e2ff-4ed6-af23-ee7225b82857'}
        ``` 
    - Notice the warning about ""--key is unset". We don't differentiate feature flag value
    based on the "key" attribute of the user. So we do not have to set it up or worry about
    this warning. 

- Scenario 2: Let's also check that the price will be 100 for users in a different country:
    - Use this command: 
        ```bash
            python3 main.py --flag "provide-discount-to-us-users" --country "North Korea"        
        ```

    - It's not a holiday in North Korea yet, so the result will be:
        ```bash
        *** Parameter --key is unset, using default key default_user

        *** The flag is on, but the user did not match any targets or rules,returning value under default rule, debug info: {'feature_flag': 'provide-discount-to-us-users'}

        *** Feature flag provide-discount-to-us-users is 100 for this user. Reason: None. Debug: None
        ``` 

## Tips on Running the CLI tool

Open your terminal and type in `python3 main.py` with arguments.

There are three possible flags you can pass in while running this script: 

- [Required Argument] To specify a flag to evaluate, pass in the flag `--flag <YOUR FLAG NAME>`
- [Optional Argument] To specify a user key
- [Optional Argument] To specify a country to evaluate, pass in the flag `--country <YOUR COUNTRY>`


Example:

```bash
python3 main.py --flag "your-flag-name" --country "United States"
```

And you will receive a response that looks like:
```bash
*** SDK successfully initialized!

*** Feature flag test-flag-one is True for this user. Reason: RULE_MATCH. Debug: {'kind': 'RULE_MATCH', 'ruleIndex': 0, 'ruleId': '47274be4-d996-48dd-bcd9-f4a76c77e736'}
```



