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

    def list_servers(self):
        return self.server.list()
    
    def find_server(self, name=None, uuid=None):
        for s in self.list_servers():
            if name:
                if s['name'] == name:
                    return s
            elif uuid:
                if s['uuid'] == uuid:
                    return s
        server_id = name or uuid
        return None
    
@click.group(name='mct')
@click.option('-v', '--verbose', is_flag=True)
@click.option('-r', '--region', type=str, default='sjc', envvar='MCT_REGION')
@click.option('-u', '--username', type=str, envvar='MCT_USERNAME')
@click.option('-p', '--password', type=str, envvar='MCT_PASSWORD')
@click.pass_context
def mct(ctx, verbose, region, username, password):
    ctx.obj = CloudSigmaContext(verbose, region, username, password)

@mct.command()
@click.argument('name', type=str, default='mailbox')
@click.option('-c', '--cpu', type=int, default=1, envvar='MCT_CPU')
@click.option('-m', '--memory', type=int, default=2, envvar='MCT_MEMORY')
@click.option('-d', '--disk', type=int, default=8, envvar='MCT_DISK')
@click.option('-k', '--key', type=str, default='mailbox', envvar='MCT_KEY')
@click.option('-i', '--install', type=str, default='OpenBSD 6.9 Install CD', envvar='MCT_INSTALL')
@click.option('-v', '--vnc-password', type=str, envvar='MCT_VNC_PASSWORD')
@click.pass_context
def create(ctx, name, cpu, memory, disk, key, install, vnc_password):

    system_drive = ctx.obj.drive.create({
        'name': f'{name}_system',
        'size': disk * 1024 ** 3,
        'media': 'disk'
    })

    host = ctx.obj.server.create({
        'name': name,
        'cpu': cpu,
        'mem': memory * 1024 ** 3,
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

    ctx.obj.server.update(host['uuid'], host)
    output(host)


@mct.command()
@click.argument('name', type=str, default='mailbox', envvar='MCT_NAME')
@click.pass_context
def show(ctx, name):
    s = ctx.obj.find_server(name)
    if s:
        output(s)
    else:
        error(f'Server {name} not found.')

@mct.command()
@click.pass_context
def list(ctx):
    for s in ctx.obj.list_servers():
        output(s)

@mct.command()
@click.argument('name', type=str, default='mailbox', envvar='MCT_NAME')
@click.option('-f', '--force', is_flag=True)
@click.pass_context
def destroy(ctx, name, force):
    s = ctx.obj.find_server(name)
    if s:
        click.echo(f"Destroy server {name} {s['uuid']}\n")
        if not force:
            if not click.confirm('Continue?'):
                click.echo('Destruction averted.')
                return
        ret = ctx.obj.server.delete(s['uuid'])
        output(ret)
    else:
        error(f'Server {name} not found.')

@mct.command()
@click.argument('name', type=str, default='mailbox', envvar='MCT_NAME')
@click.argument('path', type=str, default=None, envvar='MCT_PATH')
@click.pass_context
def backup(ctx, name, path):
    raise RuntimeError('unimplemented')

@mct.command()
@click.argument('name', type=str, default='mailbox', envvar='MCT_NAME')
@click.argument('path', type=str, default=None, envvar='MCT_PATH')
@click.pass_context
def restore(ctx, name, path):
    raise RuntimeError('unimplemented')

@mct.command()
@click.argument('name', type=str, default='mailbox', envvar='MCT_NAME')
@click.pass_context
def stop(ctx, name):
    s = ctx.obj.find_server(name)
    if s:
        ret = ctx.obj.server.stop(s['uuid'])
        output(ret)
    else:
        error(f'Server {name} not found.')


@mct.command()
@click.argument('name', type=str, default='mailbox', envvar='MCT_NAME')
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
