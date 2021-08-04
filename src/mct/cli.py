#!/usr/bin/env python3

import click
import cloudsigma
import json
import os

from pathlib import Path
from pprint import pformat

def output(item, status=True):
    click.echo(json.dumps(dict(status=status, result=item), indent=2))

def error(message):
    output(message, False)

class CloudSigmaContext(object):
    def __init__(self, verbose, region=None, username=None, password=None):
        self.verbose = verbose
        config = Path('~/.cloudsigma.conf').expanduser()
        if not config.exists():
            with config.open('w') as cfp:
                cfp.write(f"api_endpoint = https://{region}.cloudsigma.com/api/2.0/\n")
                cfp.write(f"ws_endpoint = wss://direct.{region}.cloudsigma.com/websocket\n")
                cfp.write(f"username = {username}\n")
                cfp.write(f"password = {password}\n")
        self.server = cloudsigma.resource.Server()
        self.drive = cloudsigma.resource.Drive()
        self.vlan = cloudsigma.resource.VLAN()
        self.ip = cloudsigma.resource.IP()

    def list_servers(self, detail=False):
        if detail:
            ret = self.server.list_detail()
        else:
            ret = self.server.list()
        return ret
    
    def find_server(self, name=None):
        for s in self.list_servers(True):
            if name in [s['name'], s['uuid']]:
                return s
        return None

    def list_drives(self, detail=False):
        if detail:
            ret = self.drive.list_detail()
        else:
            ret = self.drive.list()
        return ret

    def find_drive(self, name=None):
        for s in self.list_drives(True):
            if name in [s['name'], s['uuid']]:
                return s
        return None

    def list_vlans(self, detail=False):
        if detail:
            ret = self.vlan.list_detail()
        else:
            ret = self.vlan.list()
        return ret

    def find_vlan(self, name=None):
        for s in self.list_vlans(True):
            if name in [s['name'], s['uuid']]:
                return s
        return None

    def list_ips(self, detail=False):
        if detail:
            ret = self.ip.list_detail()
        else:
            ret = self.ip.list()
        return ret

    def find_ip(self, name=None):
        for s in self.list_ips(True):
            if name in [s['name'], s['uuid']]:
                return s
        return None


    def tty(self, name, kill):
        s = self.find_server(name)
        c = None
        if s:
            if kill:
                c = self.server.close_console(s['uuid'])
            else:
                c = self.server.open_console(s['uuid'])
        return c

    def convert_value(self, value):
        if value[-1] in ('g', 'G'):
            value = int(value[:-1]) * 1024 ** 3
        elif value[-1] in ('m', 'M'):
            value = int(value[:-1]) * 1024 ** 2
        else:
            value = int(value)
        return value

    def create_drive(self, name, size, media):
        return self.drive.create({
            'name': name,
            'size': size,
            'media': media
        })

    def create_server(self, name, cpu, memory, disk, key, install, vnc_password):

        memory_size = convert_value(memory)
        disk_size = convert_value(disk)
        
        system_drive = self.create_drive(f'{name}_system', disk_size, 'disk')
        
        host = self.server.create({
            'name': name,
            'cpu': cpu * 1000,
            'mem': memory_size,
            'vnc_password': vnc_password
        })

        host['drives'] = [{
            'boot_order': 1,
            'dev_channel': '0:0',
            'device': 'virtio',
            'drive': system_drive['uuid']
        }]
    
        host['nics']  = [{
            'ip_v4_conf': {
                'conf': 'dhcp',
                'ip': None
            },
            'model': 'virtio',
            'vlan': None
        }]
    
        self.server.update(host['uuid'], host)

        return host

    
@click.group(name='mct')
@click.option('-v', '--verbose', is_flag=True)
@click.option('-r', '--region', type=str, default='sjc', envvar='MCT_REGION')
@click.option('-u', '--username', type=str, envvar='MCT_USERNAME')
@click.option('-p', '--password', type=str, envvar='MCT_PASSWORD')
@click.pass_context
def mct(ctx, verbose, region, username, password):
    ctx.obj = CloudSigmaContext(verbose, region, username, password)



@mct.command()
@click.argument('resource', type=str, default='server')
@click.argument('name', type=str, default='server')
@click.option('-c', '--cpu', type=float, default=1, envvar='MCT_CPU', show_default=True)
@click.option('-m', '--memory', type=str, default='2G', envvar='MCT_MEMORY', show_default=True)
@click.option('-d', '--disk', type=str, default='8G', envvar='MCT_DISK', show_default=True)
@click.option('-k', '--key', type=str, default='server', envvar='MCT_KEY')
@click.option('-i', '--install', type=str, default='OpenBSD 6.9 Install CD', envvar='MCT_INSTALL', show_default=True)
@click.option('-v', '--vnc-password', type=str, envvar='MCT_VNC_PASSWORD')
@click.pass_context
def create(ctx, resource, name, cpu, memory, disk, key, install, vnc_password):
    """create a resource (server|drive|vlan|ip)"""

    if resource == 'server':
        s = ctx.obj.create_server(name, cpu, memory, disk, key, install, vnc_password)
    elif resource == 'drive':
        s = ctx.obj.create_drive(name, disk)
    elif resource == 'vlan':

        s = ctx.obj.create_vlan(name, addr, mask)
    elif resource == 'ip':
        s = ctx.obj.create_ip()
    else:
        s = "unable to create {resource}"
    output(s)

def find_resource(ctx, name, resource):
    s=None
    obj=None
    if resource == 'server':
        s = ctx.obj.find_server(name)
    elif resource == 'drive':
        s = ctx.obj.find_drive(name)
        obj = ctx.obj.drive
    elif resource == 'vlan':
        s = ctx.obj.find_vlan(name)
        obj = ctx.obj.vlan
    elif resource == 'ip':
        s = ctx.obj.find_ip(detail)
        obj = ctx.obj.ip
    return s,obj

@mct.command()
@click.argument('resource', type=str, default='server')
@click.argument('name', type=str, default='server', envvar='MCT_NAME')
@click.pass_context
def show(ctx, resource, name):
    """display the named resource (server|drive|vlan|ip)"""

    s, obj = find_resource(ctx, name, resource)
    if s:
        output(s)
    else:
        error(f'Resource {resource} {name} not found.')


@mct.command()
@click.argument('name', type=str, default='server', envvar='MCT_NAME')
@click.option('-k', '--kill', is_flag=True, default=False)
@click.pass_context
def tty(ctx, name, kill):
    c = ctx.obj.tty(name, kill)
    if c:
        output(c)
    else:
        error(f'Server {name} not found.')


@mct.command()
@click.pass_context
@click.argument('resource', type=str, default='servers')
@click.option('-d', '--detail', is_flag=True)
def list(ctx, resource, detail):
    """list resources (servers|drives|vlans|ips|all)"""
    result = []
    if resource in ['all', 'servers']:
        s = ctx.obj.list_servers(detail)
        result.append(s)
    if resource in ['all', 'drives']:
        s = ctx.obj.list_drives(detail)
        result.append(s)
    if resource in ['all', 'vlans']:
        s = ctx.obj.list_vlans(detail)
        result.append(s)
    if resource in ['all', 'ips']:
        s = ctx.obj.list_ips(detail)
        result.append(s)
    output(result)


@mct.command()
@click.argument('resource', type=str, default='servers')
@click.argument('name', type=str, default='server', envvar='MCT_NAME')
@click.option('-f', '--force', is_flag=True)
@click.pass_context
def destroy(ctx, resource, name, force):
    """destroy named resource (server|drive|vlan|ip)"""
    s, obj = find_resource(ctx, name, resource)
    if s:
        output(s)
        click.echo(f"Destroy {resource} {s['name']} {s['uuid']}\n")
        if not force:
            if not click.confirm('Continue?'):
                click.echo('Destruction averted.')
                return
        ret = obj.delete(s['uuid'])
        output(ret)
    else:
        error(f'Resource {resource} {name} not found.')

@mct.command()
@click.argument('name', type=str, default='server', envvar='MCT_NAME')
@click.argument('path', type=str, default=None, envvar='MCT_PATH')
@click.pass_context
def backup(ctx, name, path):
    error('unimplemented')

@mct.command()
@click.argument('name', type=str, default='server', envvar='MCT_NAME')
@click.argument('path', type=str, default=None, envvar='MCT_PATH')
@click.pass_context
def restore(ctx, name, path):
    error('unimplemented')

@mct.command()
@click.argument('name', type=str, default='server', envvar='MCT_NAME')
@click.pass_context
def stop(ctx, name):
    s = ctx.obj.find_server(name)
    if s:
        ret = ctx.obj.server.stop(s['uuid'])
        output(ret)
    else:
        error(f'Server {name} not found.')


@mct.command()
@click.argument('name', type=str, default='server', envvar='MCT_NAME')
@click.pass_context
def start(ctx, name):
    s = ctx.obj.find_server(name)
    if s:
        ret = ctx.obj.server.start(s['uuid'])
        output(ret)
    else:
        error(f'Server {name} not found.')

@mct.command()
@click.argument('server_name', type=str, default='server', envvar='MCT_NAME')
@click.argument('resource_type', type=str, default='drive', envvar='MCT_RESOURCE_TYPE')
@click.argument('resource_name', type=str, default='server_data', envvar='MCT_RESOURCE_NAME')
@click.pass_context
def attach(ctx, name):
    s = ctx.obj.find_server(name)
    if s:
        ret = ctx.obj.server.start(s['uuid'])
        output(ret)
    else:
        error(f'Server {name} not found.')

@mct.command()
@click.argument('name', type=str, default='server', envvar='MCT_NAME')
@click.pass_context
def start(ctx, name):
    s = ctx.obj.find_server(name)
    if s:
        ret = ctx.obj.server.start(s['uuid'])
        output(ret)
    else:
        error(f'Server {name} not found.')



if __name__=='__main__':
    mct()
