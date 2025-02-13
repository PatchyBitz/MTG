# Short script to try to find all non-disabled accounts.

$filename = read-host -prompt 'Output file name: '
echo "Finding active users: Outputting as: $filename"
try{
Get-ADUser -LDAPFilter '(!userAccountControl:1.2.840.113556.1.4.803:=2)' | select UserPrincipalName |% {echo $_.UserPrincipalName} |Out-File -FilePath $filename 
}
catch { echo "Going to default method - Less Reliable"
Get-ADUser -filter ("UserAccountControl -eq 512")  -Properties UserAccountControl| select UserPrincipalName |% {echo $_.UserPrincipalName} | Out-File -FilePath $filename }

$filename2 = read-host -prompt 'Output file name for non-expiring passwords: '
try{
Get-ADUser -LDAPFilter '(userAccountControl:1.2.840.113556.1.4.803:=65536)' | select UserPrincipalName |% {echo $_.UserPrincipalName} | Out-File -FilePath $filename2 }
catch{
echo "Could not get non-expiring passwords"
}

