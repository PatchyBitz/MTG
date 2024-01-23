$format = @("\b\d{3}-\d{2}-\d{4}\b","^[a-zA-Z]{2}[0-9]{2}\s?[a-zA-Z0-9]{4}\s?[0-9]{4}\s?[0-9]{3}([a-zA-Z0-9]\s?[a-zA-Z0-9]{0,4}\s?[a-zA-Z0-9]{0,4}\s?[a-zA-Z0-9]{0,4}\s?[a-zA-Z0-9]{0,3})?$","^(?:4[0-9]{12}(?:[0-9]{3})?|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})$","^@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

foreach ($num in $format)
{
    Get-ChildItem -Path "C:\" -Recurse -Include "*.txt","*.csv","*.docx" -ErrorAction SilentlyContinue |
    Select-String -Pattern $num | 
    Select Path, LineNumber
}
