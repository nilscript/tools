#!/usr/bin/env powershell.exe

Param (
    [Parameter(Mandatory = $True)][String]$VmName,
    [Parameter()][int]$RamGB = 4,
    [Parameter()][int]$Cpu = 2,
    [Parameter()][int]$DiskGB = 10,
    [Parameter()][int]$VRam = 128,
    [Parameter()][String]$OsType = "Other",
    [Parameter(Mandatory = $True)][String]$Iso,
    [Parameter()][Switch]$Force
)

function Get-VirtualBoxOsTypes {
    VBoxManage list ostypes |
    Select-String -Pattern "\GID:" |
    ForEach-Object { ($_ -replace "ID:").trim() }
}

function Get-VirtualBoxRegisteredVMs {
    VBoxManage list vms |
    Select-String -Pattern '".*"' |
    ForEach-Object { ($_.Matches.Value).trim('"') }
}

function Get-VirtualBoxVMPath {
    Param ([Parameter(Position = 0)][String]$VmName)
    VBoxManage list vms -l |
    Select-String -Pattern "Config file:.*" | 
    Select-String -Pattern ".*$VmName.*" |
    ForEach-Object { ($_.Matches.Value -replace "Config file:", "" -replace "$VmName.vbox", "").trim() }
}

if (-Not $OsType) {
    $OsType = "Other"
}
$ValidOsTypes = Get-VirtualBoxOsTypes

# Check if OsType is valid
if (-Not $($ValidOsTypes -contains $OsType)) {
    "OsType is not valid! Valid Os are: `r`n " + $ValidOsTypes
    exit 1
}

# Check if VMName is already registered 
$RegisteredVMs = Get-VirtualBoxRegisteredVMs
if ($RegisteredVMs -contains $VmName) {
    
    $title = "A virtualbox machine with name $VmName already exists."

    if (-Not $Force) {
        $question = 'Remove and continue?'

        $choices = New-Object Collections.ObjectModel.Collection[Management.Automation.Host.ChoiceDescription]
        $choices.Add((New-Object Management.Automation.Host.ChoiceDescription -ArgumentList '&Yes'))
        $choices.Add((New-Object Management.Automation.Host.ChoiceDescription -ArgumentList '&No'))

        $decision = $Host.UI.PromptForChoice($title, $question, $choices, 1)
        if ($decision -ne 0) {
            exit 1
        }
    }

    VBoxManage unregistervm $VmName --delete

}

# Create VM
VBoxManage createvm --name $VmName --ostype $OsType --register

# Specify settings
VBoxManage modifyvm $VmName --cpus $Cpu
VBoxManage modifyvm $VmName --ioapic on
VBoxManage modifyvm $VmName --boot1 dvd --boot2 disk --boot3 none --boot4 none
VBoxManage modifyvm $VmName --memory $($RamGB * 1024) --vram $VRam

# Create and attach storage 
VBoxManage storagectl $VmName --name "IDE Controller" --add ide
VBoxManage storageattach $VmName --storagectl "IDE Controller" --medium $Iso --port 0 --device 0 --type dvddrive

VBoxManage createhd --filename "$(Get-VirtualBoxVMPath $VmName)$VmName.vdi" --size $($DiskGB * 1024)
VBoxManage storagectl $VmName --name "SATA Controller" --add sata --controller IntelAHCI
VBoxManage storageattach $VmName --storagectl "SATA Controller" --medium "$(Get-VirtualBoxVMPath $VmName)$VmName.vdi" --port 0 --device 0 --type hdd 
