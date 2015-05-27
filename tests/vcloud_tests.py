from nose.tools import with_setup
from testconfig import config
from pyvcloud.vcloudair import VCA

class TestVCloud:
    
    def __init__(self):
        self.vca = None
        self.login_to_vcloud()
 
    def login_to_vcloud(self):
        """Login to vCloud"""
        username = config['vcloud']['username']
        password = config['vcloud']['password']
        service_type = config['vcloud']['service_type']
        host = config['vcloud']['host']
        version = config['vcloud']['version']
        org = config['vcloud']['org']

        self.vca = VCA(host=host, username=username, service_type=service_type, version=version, verify=True, log=True)
        assert self.vca
    
        if 'vcd' == service_type:
            result = self.vca.login(password=password, org=org)
            assert result
            result = self.vca.login(token=self.vca.token, org=org, org_url=self.vca.vcloud_session.org_url)
            assert result
        elif 'subscription' == service_type:    
            result = self.vca.login(password=password)
            assert result
        elif 'ondemand' == service_type:    
            result = self.vca.login(password=password)
            assert result
    
    def logout_from_vcloud(self):
        """Logout from vCloud"""
        print 'logout'
        selfl.vca.logout()
        self.vca = None
        assert self.vca is None
    
 
    def test_0001(self):
        """Loggin in to vCloud"""
        assert self.vca.token
    
    def test_0002(self):
        """Get VDC"""
        vdc = config['vcloud']['vdc']
        the_vdc = self.vca.get_vdc(vdc)        
        assert the_vdc
        assert the_vdc.get_name() == vdc
    
    def test_0003(self):
        """Create vApp"""
        vdc = config['vcloud']['vdc']
        vapp_name = config['vcloud']['vapp']
        vm_name = config['vcloud']['vm']
        catalog = config['vcloud']['catalog']
        template = config['vcloud']['template']
        network = config['vcloud']['network']
        mode = config['vcloud']['mode']
        the_vdc = self.vca.get_vdc(vdc)
        assert the_vdc
        assert the_vdc.get_name() == vdc
        task = self.vca.create_vapp(vdc, vapp_name, template, catalog, vm_name=vm_name)
        assert task
        result = self.vca.block_until_completed(task)
        assert result
        the_vdc = self.vca.get_vdc(vdc)
        the_vapp = self.vca.get_vapp(the_vdc, vapp_name)
        assert the_vapp
        assert the_vapp.name == vapp_name

    def test_0004(self):
        """Disconnect vApp from pre-defined networks"""
        vdc = config['vcloud']['vdc']
        vapp_name = config['vcloud']['vapp']
        the_vdc = self.vca.get_vdc(vdc)
        assert the_vdc
        assert the_vdc.get_name() == vdc
        the_vapp = self.vca.get_vapp(the_vdc, vapp_name)
        assert the_vapp
        assert the_vapp.name == vapp_name
        task = the_vapp.disconnect_from_networks()
        assert task
        result = self.vca.block_until_completed(task)
        assert result

    def test_0005(self):
        """Connect vApp to network"""
        vdc = config['vcloud']['vdc']
        vapp_name = config['vcloud']['vapp']
        vm_name = config['vcloud']['vm']
        network = config['vcloud']['network']
        mode = config['vcloud']['mode']
        the_vdc = self.vca.get_vdc(vdc)
        assert the_vdc
        assert the_vdc.get_name() == vdc
        nets = filter(lambda n: n.name == network, self.vca.get_networks(vdc))
        assert len(nets) == 1
        the_vapp = self.vca.get_vapp(the_vdc, vapp_name)
        assert the_vapp
        assert the_vapp.name == vapp_name
        task = the_vapp.connect_to_network(nets[0].name, nets[0].href)
        result = self.vca.block_until_completed(task)
        assert result

    def test_0006(self):
        """Connect VM to network"""
        vdc = config['vcloud']['vdc']
        vapp_name = config['vcloud']['vapp']
        vm_name = config['vcloud']['vm']
        network = config['vcloud']['network']
        mode = config['vcloud']['mode']
        the_vdc = self.vca.get_vdc(vdc)
        assert the_vdc
        assert the_vdc.get_name() == vdc
        nets = filter(lambda n: n.name == network, self.vca.get_networks(vdc))
        assert len(nets) == 1
        the_vapp = self.vca.get_vapp(the_vdc, vapp_name)
        assert the_vapp
        assert the_vapp.name == vapp_name
        task = the_vapp.connect_vms(nets[0].name, connection_index=0, ip_allocation_mode=mode.upper())
        result = self.vca.block_until_completed(task)
        assert result

    def test_0007(self):
        """Change vApp/VM Memory"""
        vdc = config['vcloud']['vdc']
        vapp_name = config['vcloud']['vapp']
        vm_name = config['vcloud']['vm']
        memory = config['vcloud']['memory']
        memory_new = config['vcloud']['memory_new']
        the_vdc = self.vca.get_vdc(vdc)
        assert the_vdc
        assert the_vdc.get_name() == vdc
        the_vapp = self.vca.get_vapp(the_vdc, vapp_name)
        assert the_vapp
        assert the_vapp.name == vapp_name
        details = the_vapp.get_vms_details()
        assert details[0].get('memory_mb') == memory
        task = the_vapp.modify_vm_memory(vm_name, memory_new)
        assert task
        result = self.vca.block_until_completed(task)
        assert result
        the_vapp = self.vca.get_vapp(the_vdc, vapp_name)
        assert the_vapp
        assert the_vapp.name == vapp_name
        details = the_vapp.get_vms_details()
        assert details[0].get('memory_mb') == memory_new
        
    def test_0008(self):
        """Change vApp/VM CPU"""
        vdc = config['vcloud']['vdc']
        vapp_name = config['vcloud']['vapp']
        vm_name = config['vcloud']['vm']
        cpus = config['vcloud']['cpus']
        cpus_new = config['vcloud']['cpus_new']
        the_vdc = self.vca.get_vdc(vdc)        
        assert the_vdc
        assert the_vdc.get_name() == vdc
        the_vapp = self.vca.get_vapp(the_vdc, vapp_name)
        assert the_vapp
        assert the_vapp.name == vapp_name
        details = the_vapp.get_vms_details()
        assert details[0].get('cpus') == cpus
        task = the_vapp.modify_vm_cpu(vm_name, cpus_new)
        assert task
        result = self.vca.block_until_completed(task)
        assert result
        the_vapp = self.vca.get_vapp(the_vdc, vapp_name)
        assert the_vapp
        assert the_vapp.name == vapp_name
        details = the_vapp.get_vms_details()
        assert details[0].get('cpus') == cpus_new
        
    def test_0009(self):
        """Delete vApp"""
        vdc = config['vcloud']['vdc']
        vapp_name = config['vcloud']['vapp']
        vm_name = config['vcloud']['vm']
        catalog = config['vcloud']['catalog']
        template = config['vcloud']['template']
        network = config['vcloud']['network']
        mode = config['vcloud']['mode']
        the_vdc = self.vca.get_vdc(vdc)
        assert the_vdc
        assert the_vdc.get_name() == vdc
        task = self.vca.delete_vapp(vdc, vapp_name)
        assert task
        result = self.vca.block_until_completed(task)
        assert result
        the_vapp = self.vca.get_vapp(the_vdc, vapp_name)
        assert the_vapp == None
        
        