#!/usr/bin/env python

from ansible.module_utils.basic import *
import datetime
import eapilib
EAPI_KWARG_MAP={
  'eapi_hostname': 'hostname',
  'eapi_password': 'password',
  'eapi_username': 'username',
  'eapi_port': 'port',
  'eapi_protocol': 'protocol'

}
def vlan_create(eapi, vlan_id, vlan_name):
    try:
        resource = None
        vlan_id= str(vlan_id)
        if vlan_name is not None:
            vlan_id_tmp='vlan ' + vlan_id
            vlan_name_tmp='name ' +  vlan_name
            response=eapi.config([ vlan_id_tmp,  vlan_name_tmp])
            vlan_id=int(vlan_id)
            return vlan_exist(eapi, vlan_id)
        else:
            vlan_id_tmp='vlan ' + vlan_id
            response=eapi.config([vlan_id_tmp])
            vlan_id=int(vlan_id)
            return vlan_exist(eapi, vlan_id)

    except eapilib.connections.CommandError as exc:
        if exc.message[0][0] == 1000:
            return resource
        raise



def vlan_exist(eapi, vlan_id):
    try:

        resource = None
        vlan_id=str(vlan_id)
        response=eapi.enable('show vlan %s' % vlan_id)
        resource=dict(vlanid=vlan_id, name=response[0]['vlans'][vlan_id]['name'])
         return resource
    except eapilib.connections.CommandError as exc:
        if exc.message[0][0] == 1000:
            return resource
        raise


def main():
    module=AnsibleModule(
        argument_spec=dict(
              eapi_username=dict(required=True, type='str'),
              eapi_password=dict(required=True, type='str'),
              eapi_hostname=dict(required=True),
              eapi_port=dict(required=True),
              eapi_protocol=dict(default='https'),
              state=dict(default='configured', type='str', choices=['configured', 'unconfigured', 'default']),
              vlanid=dict(required=True, type='int'),
              vlan_name=dict(default=None, type='str'),

         )

    )
kwargs=dict()
    for key, value in module.params.items():
        if value and key in EAPI_KWARG_MAP:
            kwargs[EAPI_KWARG_MAP[key]]=value

    conn=eapilib.create_connection(**kwargs)

    vlanexists=vlan_exist(conn, module.params['vlanid'])
    if vlanexists is not module.params['vlan_name']:
        vlancreate= vlan_create(conn, module.params['vlanid'], module.params['vlan_name'])
    name=module.params['vlan_name']
    result=dict(created=False, changed=False)
    result['resource']=vlan_exist(conn, module.params['vlanid'])
    module.exit_json(**result)
    #module.exit_json(name)
if __name__=="__main__":
    main()
 
