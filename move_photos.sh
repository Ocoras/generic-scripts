#!/bin/bash
# A script to copy year-month-day folders to year/month/day, useful for differing
# photo importer outputs
start=$1
dest=$2
orig="$PWD"
echo Moving: $start into $dest
cd $start
folders_to_be_moved=$( ls */ -d )
cd "$orig"
echo Contents = $folders_to_be_moved

for folder in $folders_to_be_moved
do
  dates=($(echo $folder | tr "-" "\n"))

  day=${dates[0]}
  month=${dates[1]}
  # remove the trailing back slash on year:
  year=${dates[2]::-1}
  # echo Folder: $folder   year: $year month: $month day: $day
  new_loc=$(echo "$dest/$year/$month/$day/")

  # echo Copy into "$dest/$year/$month/$day/"?
  # read ans
  # if [[ $ans = y ]]; then
    #statements
  mkdir -p "$dest/$year/$month/$day/"
  echo Moving $folder to "$dest/$year/$month/$day/"
  mv "$start/$folder"* "$dest/$year/$month/$day/"
  rmdir "$start/$folder"
  # fi
done
