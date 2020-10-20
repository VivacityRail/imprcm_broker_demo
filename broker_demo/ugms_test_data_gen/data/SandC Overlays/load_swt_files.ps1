# load all the SWT files to database

# iterate through all the .csv.gz files in the source data folder and load them to the PostgreSQL database

# needs 7-zip https://www.7-zip.org/

$Start_folder = "D:\Network Rail\UTGM Data\Input Data\DC159-012"
# $Start_folder = "D:\GithubRepos\IMPRCM\broker\Testing\SampleData\SWT"

# truncate the database table
& psql -h vivienne01 -U pete -d imprcm_demo_raw -c "truncate table raw_ugms_swt"


get-childitem -path $Start_folder -filter *csv.gz | foreach-object {

    $file = $_
    $filename = $file.fullname
    $folder = (get-item $file.directory).fullname   
    $csv_file = $file.basename

    # write-host $filename ($folder + "\" + $csv_file)

    # extract the zip file contents
    & 'C:\Program Files\7-Zip\7z.exe' e -y -bb0 $filename 

    # command for psql - uses the FROM PROGRAM option to pass the data through the python script
    $cmd = "\copy raw_ugms_swt from program 'python .\process_raw_swt_ugms.py " + $csv_file + "' with (format CSV, header False)"
    # write-host $cmd

    # load the data to database
    & psql -h vivienne01 -U pete -d imprcm_demo_raw -c $cmd

    # delete the csv file
    remove-item $csv_file

}

