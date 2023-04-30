@plugin.method("nostr_node_announcement")
def nostr_node_announcement(plugin):
    """ Creates the node annoucnemnt note """
    npub = plugin.pubkey
    info = plugin.rpc.getinfo()
    id_pub = info['id']
    network = info['network']
    attestation = plugin.rpc.signmessage(npub)
    nostrify_log("creating node announcement")
    plugin.publisher.publish_node_announcement(id_pub, attestation, network, npub)

    return f"npub: {npub} attestation: {attestation}"


@plugin.method("nostr_verify_announcement")
def verify_nostr_node_announcement(plugin, node_announcement):
    """ Verifies a node annoucnemnt """
    message = "npub1u908w53asa6jm4d0atzj2qggjjkhas2grmpqc930ctklv8hyzlus79sr2v"
    signature  = "rbfbd5k7rcpkiypgqr44aadfuj6wjquywqxztaef68ds957xtrjx6fjnuw7geftfykkiw7ucy3zouussjhpyr4qka1w6a8prgdqfr5bw"
    pubkey = plugin.pubkey
    check_attestation(message, signature, pubkey)


@plugin.method("nostr_sync_graph")
def nostr_node_announcement(plugin):
    """ Pulls graph data from nostr relay and funnels into gossip """
    nostrify_log("Syncing graph")
    return "synced"




# Options


plugin.add_option('nostr_relay',
                  description="The relay you want to send events to",
                  default=[],
                  multi=True,
                  opt_type='string')

plugin.add_option('nostr_pubkey',
                  default='',
                  description='The Nostr pubkey you want to send events to',
                  opt_type='string')

plugin.add_option('nostr_disable_event',
                  description='The CLN events you do NOT want to receive on Nostr (default will send all events)',
                  default=[],
                  multi=True,
                  opt_type='string')
plugin.run()