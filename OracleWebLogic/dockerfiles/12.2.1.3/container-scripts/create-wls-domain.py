domain_name  = os.environ.get("DOMAIN_NAME", "uber")
admin_name  = os.environ.get("ADMIN_NAME", "AdminServer")
admin_username  = os.environ.get("ADMIN_USERNAME", "weblogic")
admin_pass  = "ADMIN_PASSWORD"
admin_port   = int(os.environ.get("ADMIN_PORT", "7001"))
domain_path = os.environ.get("DOMAIN_HOME", '/u01/oracle/user_projects/domains/%s' % domain_name)
production_mode = os.environ.get("PRODUCTION_MODE", "dev")

print('domain_name     : [%s]' % domain_name);
print('admin_port      : [%s]' % admin_port);
print('domain_path     : [%s]' % domain_path);
print('production_mode : [%s]' % production_mode);
print('admin name      : [%s]' % admin_name);
print('admin username  : [%s]' % admin_username);

# Open default domain template
# ======================
readTemplate("/u01/oracle/wlserver/common/templates/wls/wls.jar")

set('Name', domain_name)
setOption('DomainName', domain_name)

# Disable Admin Console
# --------------------
cmo.setConsoleEnabled(false)

# Configure the Administration Server and SSL port.
# =========================================================
cd('/Servers/AdminServer')
set('Name', admin_name)
set('ListenAddress', '')
set('ListenPort', admin_port)
set('TunnelingEnabled', 'true')
set('ExternalDNSName', 'wls-uber.k8s.ctnrva0.dev.vonagenetworks.net')
logMBean = create('AdminServer', 'Log')
logMBean.setRedirectStderrToServerLogEnabled(0)
logMBean.setRedirectStdoutToServerLogEnabled(0) 
logMBean.setLog4jLoggingEnabled(1)

# Define the user password for weblogic
# =====================================
cd('/Security/%s/User/weblogic' % domain_name)
cmo.setPassword(admin_pass)

# Write the domain and close the domain template
# ==============================================
setOption('OverwriteDomain', 'true')
setOption('ServerStartMode',production_mode)

cd('/NMProperties')
set('ListenAddress','')
set('ListenPort',5556)
set('CrashRecoveryEnabled', 'true')
set('NativeVersionEnabled', 'true')
set('StartScriptEnabled', 'false')
set('SecureListener', 'false')
set('LogLevel', 'FINEST')

# Set the Node Manager user name and password (domain name will change after writeDomain)
cd('/SecurityConfiguration/base_domain')
set('NodeManagerUsername', admin_username)
set('NodeManagerPasswordEncrypted', admin_pass)

# Write Domain
# ============
writeDomain(domain_path)
closeTemplate()

# Exit WLST
# =========
exit()

