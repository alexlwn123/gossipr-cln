#!/usr/bin/env python3

import os
from pyln.client import Plugin
from nostr.key import PrivateKey
from nostr_publisher import NostrPublisher

plugin = Plugin()


def post_node_announcement(content):
    """ Sends `content` as a Nostr Event"""
    if os.environ.get('TEST_DEBUG') is not None:
        nostrify_log(content)
    else:
        plugin.publisher.publish_node_announcement(content)

def send_nostr_event(content):
    """ Sends `content` as a Nostr Event"""
    if os.environ.get('TEST_DEBUG') is not None:
        nostrify_log(content)
    else:
        plugin.publisher.publish_dm_content(content)


def nostrify_log(message):
    """ Logs a message to the plugin log """
    plugin.log(f"[Nostrify]: {message}")


def check_attestation(message, signature, pubkey):
    """ Verfies a signature from another lightning node """
    verfication = plugin.rpc.checkmessage(message, signature, pubkey)
    return verification


@plugin.init()
def init(options, configuration, **kwargs):
    """ Initializes the plugin """

    plugin.secret = plugin.rpc.makesecret(string='nostr')['secret']

    #plugin.relays = options['nostr_relay']
    plugin.relays = ['wss://nostr-relay']

    nostrify_log(f"set to use relays: {plugin.relays}")

    #plugin.pubkey = options['nostr_pubkey']

    plugin.disabled_events = options['nostr_disable_event']
    nostrify_log(f"set to ignore events: {plugin.disabled_events}")

#    if plugin.relays is None:
#        nostrify_log(
#            "must set at least one relay with the `nostr_relay` option")
#        return

    try:
        plugin.publisher = NostrPublisher(
            plugin.relays, plugin.secret, plugin.pubkey)
    except Exception as e:
        nostrify_log(
            "an error occurred while initializing the NostrPublisher:")
        nostrify_log(str(e))
        return

    nostrify_log("plugin initialized")


# Methods

@plugin.method("nostr_gen_keys")
def generate_nostr_keys(plugin):
    """ Returns the node's pubkey """
    private_key = PrivateKey(bytes.fromhex(plugin.secret))
    public_key = f"{private_key.public_key.bech32()}"
    plugin.pubkey = public_key
    plugin.privkey = private_key
    plugin.log(f'pubkey {plugin.pubkey}')
    nostrify_log(f"returning public_key: {public_key}")
    return f'pub: {public_key} priv: {private_key}'

@plugin.method("nostr_follow_peers")
def follow_peersplugin(plugin):
    """ Follows gossip peers on nostr """
    peers = plugin.rpc.listpeers()
    nostrify_log(f"peers: {peers}")
    return peers

@plugin.method("nostr_node_announcement")
def nostr_node_announcement(plugin):
    """ Creates the node annoucnemnt note """
    npub = plugin.pubkey
    info = plugin.rpc.getinfo()
    id_pub = info['id']
    network = info['network']
    attestation = plugin.rpc.signmessage(npub)
    nostrify_log("creating node announcement")
    node_announcement = {'ip': id_pub, 's': attestation, 'n': network}
    post_node_announcement(str(node_announcement))

    #plugin.publisher.publish_node_announcement(id_pub, attestation, network, npub)

    return f"npub: {npub} attestation: {attestation} network: {network}"


@plugin.method("nostr_verify_announcement")
def verify_nostr_node_announcement(plugin, node_announcement):
    """ Verifies a node annoucnemnt """
    message = "npub1u908w53asa6jm4d0atzj2qggjjkhas2grmpqc930ctklv8hyzlus79sr2v"
    signature  = "rbfbd5k7rcpkiypgqr44aadfuj6wjquywqxztaef68ds957xtrjx6fjnuw7geftfykkiw7ucy3zouussjhpyr4qka1w6a8prgdqfr5bw"
    pubkey = plugin.pubkey
    check_attestation(message, signature, pubkey)

@plugin.method("test_push")
def nostr_node_announcement(plugin):
    """ Pulls graph data from nostr relay and funnels into gossip """
    send_nostr_event('testy')

    return "synced"

@plugin.method("nostr_sync_graph")
def nostr_node_announcement(plugin):
    """ Pulls graph data from nostr relay and funnels into gossip """
    nostrify_log("Syncing graph")
    return "synced"



# Options


plugin.add_option('nostr_relay',
                  description="The relay you want to send events to",
                  default=['wss://eden.nostr.land'],
                  multi=True,
                  opt_type='string')

plugin.run()