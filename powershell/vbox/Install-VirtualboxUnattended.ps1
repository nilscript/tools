#!/usr/bin/env powershell.exe

Param (
    [Parameter(Mandatory = $True)][String]$VmName, 
    [Parameter(Mandatory = $True)][String]$Username,
    [Parameter(Mandatory = $True)][String]$Fullname,
    [Parameter(Mandatory = $True)][String]$Iso,
    [Parameter(Mandatory = $True)][Security.SecureString]$Password,
    [Parameter(Mandatory = $True)][String]$TimeZone 
)

VBoxManage unattended install $VmName --iso $Iso `
    --user=$Username --full-user-name $Fullname --password=$Password `
    --time-zone=$TimeZone --install-additions 

VBoxManage startvm $VmName
