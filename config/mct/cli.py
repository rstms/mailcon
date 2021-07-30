#!/usr/bin/env python3

import click

@click.group(name='mct')
@click.argument('command', type=str, default='help')
@click.option('-v', '--verbose', is_flag=True)
def mct(ctx, **kwargs):
    ctx.obj=dict(ctx.params)

@mct.command()
@click.argument('name', type=str, default='mailbox')
@click.option('-m', '--memory', type=int, default=2)
@click.option('-d', '--disk', type=int, default=8)
@click.option('-k', '--key', type=str, default='mailbox')
@click.option('-i', '--install', type=str, default='OpenBSD 6.9 Install CD')
def create(ctx, name, memory, disk, key, install):
    click.echo('create')

@mct.command()
def list(ctx):
    click.echo('create')
    raise RuntimeError('unimplemented')

@mct.command()
@click.argument('name', type=str, default='mailbox')
def destroy(ctx, name):
    raise RuntimeError('unimplemented')

@mct.command()
@click.argument('name', type=str, default='mailbox')
@click.argument('path', type=str, default=None)
def backup(ctx, name, path):
    raise RuntimeError('unimplemented')

@mct.command()
@click.argument('name', type=str, default='mailbox')
@click.argument('path', type=str, default=None)
def restore(ctx, name, path):
    raise RuntimeError('unimplemented')

@mct.command()
@click.argument('name', type=str, default='mailbox')
def stop(ctx, name):
    raise RuntimeError('unimplemented')

@mct.command()
@click.argument('name', type=str, default='mailbox')
def start(ctx, name):
    raise RuntimeError('unimplemented')
