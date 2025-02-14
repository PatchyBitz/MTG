
#$file =  Read-Host("File to users: ")
$delimit = "|"
Get-Content -Path Reset.csv | ForEach-Object{Set-ADAccountPassword -Identity $_.split("|")[0] -Reset -NewPassword (ConvertTo-SecureString -AsPlainText $_.split($delimit)[1] -Force)}
# % { echo "User is: " $_.split('|')[0]   "