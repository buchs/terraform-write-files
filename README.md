# terraform-write-files

This is a simple Terraform module that creates a data source which writes files to disk. This lets you write files with any value, primarily for debugging purposes, during Terraform's plan stage.

## Usage

```js
module "write_files" {
  source = "github.com/claranet/terraform-write-files"

  files = {
    "bastion-new.txt" = "${data.template_file.bastion_user_data.rendered}"
    "web-new.txt"     = "${data.template_file.web_user_data.rendered}"
  } 
}
```

## Full Example

You see the following output from `terraform plan`:

```sh
-/+ module.bastion.aws_launch_configuration.lc (new resource required)
      user_data: "a3c8232429b62c18ab9dd5a6e6f6a7b9f2dcafb7" => "646874fb1ffffc303a1138963a5f7c17216d9b99" (forces new resource)
```

All you can tell from this is that the user data will change, but you don't see how it will change.

You can use this module to write the new user data value to a file, and then compare it to the launch configuration's user data value.

```sh
# Get the current user data.
$ aws autoscaling describe-launch-configurations --launch-configuration-name $BASTION_LAUNCH_CONFIG_NAME --query 'LaunchConfigurations[0].UserData' --output text | base64 -d > bastion-old.txt

# Run terraform with this module to get the new user data.
$ terraform plan

# Check that the hashes match those from the plan.
$ sha1sum bastion-old.txt bastion-new.txt 
a3c8232429b62c18ab9dd5a6e6f6a7b9f2dcafb7  bastion-old.txt
646874fb1ffffc303a1138963a5f7c17216d9b99  bastion-new.txt

# Now compare the files and see what will change.
$ diff bastion-old.txt bastion-new.txt 
16c16
<   ephemeral_devices="$$ephemeral_devices /dev/${edev}"
---
>   ephemeral_devices="$ephemeral_devices /dev/${edev}"
```
