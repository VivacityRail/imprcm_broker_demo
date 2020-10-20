# load test data files to database

# iterate through all the Geometry .csv.gz files in the source data folder, convert to IMPRCM format, 

# needs 7-zip https://www.7-zip.org/

param(
    [string] $start_folder = '.',
    [string] $temp_folder = '..\data\temp',
    [string] $output_folder = '..\data\inbox',
    )


# iterate through the geometry csv.gz files, converting each to imprcm format
get-childitem -path $start_folder -filter Geometry*csv.gz | foreach-object {

    $file = $_
    $filename = $file.fullname
    $folder = (get-item $file.directory).fullname   
    $csv_file = $file.basename
    # output file has  uuid_<csv_file_name>
    $out_file = [guid]::newguid().tostring() + '_' + $csv_file

    write-host $csv_file
    write_host $out_file
    # write-host $filename ($folder + "\" + $csv_file)

    # extract the zip file contents
    & 'C:\Program Files\7-Zip\7z.exe' e -y -bb0 -o"$temp_folder" $filename > $null

    # convert using the adapter create_imprcm_format_ugms_csv_from_swt.py
    python .\from_swt\create_imprcm_format_ugms_csv_from_swt.py "$($temp_folder + '\' + $csv_file)" --outputfolder="$($output_folder)" --outputfile="$($out_file)"

    # zip up the output csv file

    # FIX THIS!!!
    & 'C:\Program Files\7-Zip\7z.exe' a -y -bb0 -o"$temp_folder" $filename > $null


   
    # delete the csv file
    remove-item "$($temp_folder + '\' + $csv_file)"

}

