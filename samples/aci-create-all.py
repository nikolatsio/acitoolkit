#!/usr/bin/env python
"""
Sample of creating a Tenant, App Profile, EPG, VRF, BridgeDomain
"""

from acitoolkit.acitoolkit import *


def main():
    """
    Main execution routine

    :return: None
    """
    creds = Credentials('apic')
    creds.add_argument('--tenant', help='The name of Tenant')
    creds.add_argument('--aprofile', help='The name of the Application Profile')
    creds.add_argument('--epg', help='The name of EPG')
    creds.add_argument('--epgdescr', help='description of EPGs')
    creds.add_argument('--vrf', help='The name of VRF')
    creds.add_argument('--bd', help='The name of BridgeDomain')
    creds.add_argument('--address', help='Subnet IPv4 Address')
    creds.add_argument('--scope', help='The scope of subnet ("public", "private", "shared", "public,shared", "private,shared", "shared,public", "shared,private")')
    creds.add_argument('--json', const='false', nargs='?', help='Json output only')
    creds.add_argument('--delete', action='store_true', help='Delete the configuration from the APIC')

    args = creds.get()
    session = Session(args.url, args.login, args.password)
    session.login()

    tenant = Tenant(args.tenant)
    app = AppProfile(args.aprofile, tenant)
    epg = EPG(args.epg, app)
    epg.descr=(args.epgdescr)
    vrf = Context(args.vrf, tenant)
    bd = BridgeDomain(args.bd, tenant)
    bd.add_context(vrf)
    epg.add_bd(bd)

    if args.address is None:
        bd.set_arp_flood('yes')
        bd.set_unicast_route('no')
    else:
        bd.set_arp_flood('no')
        bd.set_unicast_route('yes')

        subnet = Subnet('test', bd)
        subnet.addr = args.address

        if args.scope is None:
            subnet.set_scope("private")
        else:
            subnet.set_scope(args.scope)

    if args.delete:
        tenant.mark_as_deleted()


    if args.json:
        print(tenant.get_json())
    else:
        resp = session.push_to_apic(tenant.get_url(),
                                    tenant.get_json())

        if not resp.ok:
            print('%% Error: Could not push configuration to APIC')
            print(resp.text)

if __name__ == '__main__':
    main()
