Fork of CLN plugin: Nostrify <https://github.com/joelklabo/nostrify>

```
RPC methods
===========

Plugins may provide additional RPC methods that you can simply
call as if they were built-in methods from lightningd
itself. To call them just use lightning-cli or any other
frontend. The following methods are defined by this plugin:

  nostr_gen_keys
    No documentation found

  nostr_follow_peers
    No documentation found

  nostr_node_announcement
    No documentation found

  nostr_verify_announcement
    No documentation found

  nostr_sync_graph
    No documentation found

Command line options
====================

This plugin exposes the following command line options. They
can be specified just like any other you might gice lightning
at startup. The following options are exposed by this plugin:

  --nostr_relay=string  (default: ['wss://eden.nostr.land']
    The relay you want to send events to

    This option can be specified multiple times
```
