
param(
    [string] $start_folder = '.'
    )



Get-ChildItem -path $start_folder -filter *Geometry*.csv  | foreach-object { 
    $file = $_
    $filename = $file.fullname
    # $folder = (get-item $file.directory).fullname   
    $archive_file = $start_folder + "\" + $file.name + ".gz"

    write-host $filename $archive_file 
    & 'C:\Program Files\7-Zip\7z.exe' a -y -tgzip -bb0 -sdel  $archive_file $filename
}
