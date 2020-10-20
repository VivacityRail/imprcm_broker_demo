# Create a powershell script which will create a batch of these files simulating data generated by a single unit over a series of dates, 
# creating each file with an appropriate filename.

# Run the script using a database set up in the parallel task  to define the test data in terms of base geometry and overlays so that it matches (some of) the S&C units on the Paddington to Reading line and simulates degradation and repair of these units.

param(
    [string] $start_folder = '.',
    [string] $scenario_file,
    [string] $destination_folder = '.',
    [int] $debug = 0
    )

if ($debug -eq 1) {$db = "--debug"} else {$db = "" } 
# read the scenario file, run the test data generator for each line of scenario data
write-host "debug" $db
$m = import-csv($scenario_file) -Delimiter "`t"    
$m | foreach-object{ python .\test_generator.py "--unit" $_.unit "--rundate" $_.date $db $_.database  }

# zip the files up
md $destination_folder > $null

Get-ChildItem -path $start_folder -filter *Geometry*.csv  | foreach-object { 
    $file = $_
    $filename = $file.fullname
    # $folder = (get-item $file.directory).fullname   
    $archive_file = $destination_folder + "\" + $file.name + ".gz"

    write-host $filename $archive_file $destination_folder
    & 'C:\Program Files\7-Zip\7z.exe' a -y -tgzip -bb0 -sdel  $archive_file $filename
}
