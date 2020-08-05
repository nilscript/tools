#!/usr/bin/env powershell.exe

while ($true) { 
    Get-Process 
    | Sort-Object -Descending cpu 
    | Select-Object -First 15 
    | Format-Table -AutoSize
    
    Start-Sleep 5
    Clear-Host 
}
