vepath = "/home/vagrant/pymysqlreplication2.7"

python_virtualenv vepath do
    interpreter "python2.7"
    owner "vagrant"
    group "vagrant"
    action :create
end

python_pip "pymysql" do
    virtualenv vepath
    action :install
end
