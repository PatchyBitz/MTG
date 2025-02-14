# Short script to try to do some basic recond.



$file = read-host -prompt 'Recon Output file name: '

$file2 = read-host -prompt 'Output file for distinguished names'
echo "Finding active users: Outputting as: $file"
echo "=================== Found Active Users ===================" | Out-File  -FilePath ($file) -Append

try{
Get-ADUser -LDAPFilter '(!userAccountControl:1.2.840.113556.1.4.803:=2)' | select samAccountName |% {echo $_.samAccountName} |Out-File -FilePath $file -Append
}
catch { echo "Going to default method - Less Reliable"
Get-ADUser -filter ("UserAccountControl -eq 512")  -Properties UserAccountControl| select samAccountName |% {echo $_.samAccountName} | Out-File -FilePath $file -Append }




echo "=================== Users Without Required Passwords ===================" | Out-File  -FilePath ($file) -Append

Get-ADUser -Filter {PasswordNotRequired -eq $true} |% { }|Out-File  -FilePath ($file) -Append




echo "=================== Users with Non-Expire Passwords ===================" | Out-File  -FilePath ($file) -Append

try{
Get-ADUser -LDAPFilter '(userAccountControl:1.2.840.113556.1.4.803:=65536)' | select UserPrincipalName |% {echo $_.UserPrincipalName} | Out-File -FilePath $file -Append }
catch{
echo "Could not get non-expiring passwords"
}
echo "=================== Users with Login Scripts ===================" | Out-File  -FilePath ($file) -Append

try{
Get-ADUser -Filter {scriptPath -like '*'} -Properties scriptPath| % { "$($_.UserPrincipalName) - Path: $($_.scriptPath)" } | Out-File -FilePath $file -Append 

}
catch{
echo "Error with getting users with login scripts"
}


#Block to output Distiguished Names for Password resets
echo "Writing Distinguished Names in: $file2"
try{
Get-ADUser -LDAPFilter '(!userAccountControl:1.2.840.113556.1.4.803:=2)' | select DistinguishedName |% {echo $_.DistinguishedName} |Out-File -FilePath $file2 
}
catch { echo "Going to default method - Less Reliable"
Get-ADUser -filter ("UserAccountControl -eq 512")  -Properties UserAccountControl| select DistinguishedName |% {echo $_.DistinguishedName} | Out-File -FilePath $file2  }