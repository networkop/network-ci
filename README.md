# NETWORK-CI

## Proof of Concept of CI/CD methodology applied to traditional non-SDN network topologies

This repository contains a set of tools that can be used to automate network testing during design and upgrade stages.
This is what these tools can do for you:

* Build full network topology inside a network emulation environment
* Apply configuration to all built nodes
* Verify real-time connectivity between nodes while making manual configuration changes
* Verify traffic flows against pre-defined rules
* Shutdown and delete the network topology

These tools can be combined and used by CI/CD automation servers like Jenkins as I showed in my [blog](http://networkop.github.io/blog/2016/02/19/network-ci-intro/).

## Examples

 To show how these tools can be used, I've created the following sample networks ranging in size from 4 to 14 nodes.

* [acme-small](/acme-small) - simple 4-node topology
* [acme-large](/acme-large) - 14-node enterprise data centre

## Documentation

For detailed instructions on how to use these tool proceed to [skeleton](/skeleton/)

