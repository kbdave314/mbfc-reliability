{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let
  packageSet = ps: with ps; [

    ## for fetching:
    certifi
    urllib3

    ## for parsing:
    pyquery
    uritools
  ];
  drv = python36.withPackages packageSet;
in
  drv.env

