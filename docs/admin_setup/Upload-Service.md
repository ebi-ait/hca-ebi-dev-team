# Upload Service

## Development Notes

### Configuring Environment for Existing Deployment

Setting up local environment requires exactly the following versions of the following tools:

* Terraform v0.11.13

  To easily facilitate switching between versions of Terraform, consider installing tools like [`tfswtich`](https://warrensbox.github.io/terraform-switcher/).

* Python 3.6

  For switching Python environments, use tools like `pyenv`, `virtualenv`, etc. or combinations of such.


#### Setting Up the environment

1. Clone or add remote reference to the
[Upload Service repository](http://github.com/ebi-ait/upload-service.git).
2. Install required Python modules.

  ```
  pip install -r requirements.txt
  pip install -r requirements-dev.txt
  ```

3. Apply environment config:

  ```
  source config/environment <dev|staging|prod>
  ```

4. Go to `terraform/envs/<dev|staging|prod>`. 
5. Retrieve previously defined Terraform variables:

  ```
  make retrieve-vars
  ```

6. Finally, initialise local Terraform installation:

  ```
  make init
  ```

#### Making changes to terraform config
1. After making changes to terraform config, go to `terraform` dir
```
cd  <base-dir>/upload-service/terraform
make apply
```
2. Test the changes
3. Go to `terraform/envs/<dev|staging|prod>`
```
make upload-vars
```