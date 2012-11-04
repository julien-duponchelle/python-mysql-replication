maintainer        "Julien Duponchelle"
maintainer_email  "julien@duponchelle.info"
license           "Apache 2.0"
description       "Installs Virtual envs for testing pymysql replication."
version           "0.0.1"

depends           "python"

recipe "pymysqlreplication-test", "Installs python, pip, and virtualenv"

%w{ ubuntu }.each do |os|
  supports os
end
