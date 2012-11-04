# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise64"

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.provision :chef_solo do |chef|
     chef.cookbooks_path = ["vagrantchef/cookbooks", "vagrantchef/site-cookbooks"]
     chef.roles_path = "vagrantchef/roles"
     chef.data_bags_path = "vagrantchef/data_bags"
     chef.add_recipe "git"
     chef.add_recipe "python"
     chef.add_recipe "mysql::client"
     chef.add_recipe "mysql::server"
     chef.add_recipe "pymysqlreplication-test"
  #   chef.add_role "web"
  #
  #   # You may also specify custom JSON attributes:
    chef.json = {
        :mysql => {
            :bind_address => "127.0.0.1",
            :tunable => {
                :log_bin => "mysql-bin.log"
            },
            :server_root_password => "",
            :server_repl_password => "",
            :server_debian_password => "maint"
        }
    }
  end
end
