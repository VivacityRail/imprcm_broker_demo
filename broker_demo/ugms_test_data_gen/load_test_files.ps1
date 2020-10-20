# load test data files to database

# iterate through all the .csv.gz files in the source data folder and load them to the PostgreSQL database

# needs 7-zip https://www.7-zip.org/

param(
    [string] $start_folder = '.'
    )


$HOST_NAME = 'vivienne01'
$DATABASE = 'imprcm_demo_ugms_touchdown'
$TARGET_TABLE = 'ugms_touchdown'

#  $Start_folder = "D:\Network Rail\UTGM Data\Input Data\DC159-012"
# $Start_folder = "D:\GithubRepos\IMPRCM\broker\Testing\SampleData\SWT"

# truncate the database table
& psql -h $HOST_NAME -U pete -d $DATABASE -c "truncate table $TARGET_TABLE"

# iterate through the geometry csv.gz files, loading each to database
get-childitem -path $start_folder -filter Geometry*csv.gz | foreach-object {

    $file = $_
    $filename = $file.fullname
    $folder = (get-item $file.directory).fullname   
    $csv_file = $file.basename

    write-host $csv_file
    # write-host $filename ($folder + "\" + $csv_file)

    # extract the zip file contents
    & 'C:\Program Files\7-Zip\7z.exe' e -y -bb0 $filename 

    # command for psql - uses the FROM PROGRAM option to pass the data through the python script
    $cmd = "\copy ugms_touchdown from program 'python .\create_imprcm_format_ugms_csv_from_swt.py " + $csv_file + "' with (format CSV, header True)"
 
    # load the data to database
    & psql -h vivienne01 -U pete -d imprcm_demo_ugms_touchdown -c $cmd

    # update the file log
    $cmd = "insert into files_loaded (file_name, loaded_timestamp) values ('" + $csv_file + "', current_timestamp)"
    # write-host $cmd
    & psql -h vivienne01 -U pete -d imprcm_demo_ugms_touchdown -c $cmd

    # process the file

     & psql -h vivienne01 -U pete -d imprcm_demo_ugms_touchdown -f 'D:\GithubRepos\IMPRCM\broker\DataDefinition\Processing\load_wanted_sandc_geom_data.sql'
 
    # delete the csv file
    remove-item $csv_file

}

