"""Instantiates nodes of c6525-100g type."""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Parameters:
portal.context.defineParameter("n_nodes", "Number of nodes", portal.ParameterType.INTEGER, 8)

params = portal.context.bindParameters()

def cmd(node, command):
    node.addService(pg.Execute("/bin/sh", command))

# Create nodes
nodes = []
interfaces = []

for i in range(params.n_nodes):
    node = request.RawPC("node-" + str(i))
    node.hardware_type = "c6525-100g"
    node.disk_image = "urn:publicid:IDN+utah.cloudlab.us+image+uic-dcs-PG0:c6525-100g-8.node-0:1"
    node.Desire('connected-to-edgecore1', 1.0)

    # format disk
    # TODO
    cmd(node, "echo 'y' | sudo mkfs.ext4 /dev/nvme1n1")
    
    # add interface
    interface = node.addInterface('interface-' + str(i))
    nodes.append(node)
    interfaces.append(interface)

# Link link-0
link_0 = request.Link('link-0')
link_0.Site('undefined')

for iface in interfaces:
    link_0.addInterface(iface)
    
for node in nodes:
    node.installRootKeys(True, True)
    
# Print the generated rspec
pc.printRequestRSpec(request)
