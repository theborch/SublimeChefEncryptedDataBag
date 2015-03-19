# ChefEncryptedDataBag

Sublime Text 2/3 Plugin to encrypt/decrypt [chef](https://www.chef.io/chef/) encrypted data item.

# Requirements

- ruby >= 1.9
- chef gem 11.12.4 tested

You can specify ruby path.
Please copy `ChefEncryptedDataBag.sublime-settings` to `Packages/User/ChefEncryptedDataBag.sublime-settings` and edit it.

# Usage

1. Open chef repository directory that have `data_bag_key` file.
2. Open encrypted/plain data bag item (JSON).
3. Open command palette (`command + shift + p`) and run `Chef: Encrypt/Decrypt data bag item`

# License

MIT License.
Copyright 2015 labocho.
