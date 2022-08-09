#!/bin/bash

ROOT=/mnt/e/ROMVault
DAT_ROOT=${ROOT}/DatRoot
OTHERDAT_ROOT=${ROOT}/OtherDats

./parseredump.py

FILES="bios
cues
gdi
datfile
sbi"

for f in $FILES; do
	if [[ -d "$f" ]]; then
		rm -rf $f
	fi
	mkdir $f
	cd $f
	aria2c --file-allocation=prealloc -i ../$f.txt
	cd ..
done
echo Uncompressing Datfiles
cd ${DAT_ROOT}/Consoles/Redump
for f in ${OTHERDAT_ROOT}/Redump/datfile/*.zip; do
	case $f in
	  	*"IBM - PC compatible"*|*"Apple - Macintosh"*|*"Microsoft - Xbox"*|*"Sony - PlayStation 2"*)
		# echo "Paila-$f"
	    ;;
  		*)
		# echo "SI-$f"
    	unzip -o "$f";
	    ;;
	esac
done

echo Copying Bios Datfiles
cd ${DAT_ROOT}/Consoles/Redump-bios
cp ${OTHERDAT_ROOT}/Redump/bios/* .

echo Sending TrrntZipping cues to Background
cd ${OTHERDAT_ROOT}/Redump/cues
(ls -1a | parallel -j 8 TrrntZip > /dev/null 2>&1 & )

#############################################################################################
#### Aqui voy
#############################################################################################

cd /mnt/e/ROMVault/FixDats
echo Deduping Datfiles
./dedupdats.py
echo Merging Datfiles
./mergedats.py
echo Creating Lists
./allmissings.py


cd ${DAT_ROOT}/Consoles/No-Intro
preffixes=(""
"Unofficial - "
"Non-Redump - ")

unwanted=("IBM - PC and Compatibles (Digital)"
"Microsoft - XBOX 360 (Digital)"
"Nintendo - Nintendo 3DS (Decrypted)"
"IBM - PC Compatible (Discs)"
"Microsoft - Microsoft Xbox 360"
"Nintendo - Nintendo 3DS (Digital) (CDN)"
"Non-Redump - Nintendo - Wii"
"Nintendo - Wii U (Digital) (CDN)"
"Non-Redump - Sony - PlayStation 2"
"Sony - PlayStation 3 (PSN)"
"Sony - PlayStation Mobile (PSN)"
"Sony - PlayStation Portable (PSN) (Encrypted)"
"Nintendo - Nintendo 3DS (Digital) (Updates and DLC) (Decrypted)"
"Unofficial - Nintendo - Nintendo DSi (Digital)"
"Sony - PlayStation (PS one Classics) (PSN)"
"Sony - PlayStation 3 (PSN) (Decrypted)"
"Sony - PlayStation Portable (PSN) (Decrypted)"
"Sony - PlayStation Portable (PSX2PSP)"
"Sony - PlayStation Portable (UMD Video)"
"Sony - PlayStation Vita (BlackFinPSV)"
"Sony - PlayStation Vita (NoNpDrm)"
"Sony - PlayStation Vita (PSN)"
"Sony - PlayStation Vita (PSVgameSD)"
"Sony - PlayStation 3"
)

for d in *.dat; do
	for i in "${unwanted[@]}"; do
		replaced=${d/"$i"/nada}
		if [ "$d" != "$replaced" ]; then
			# echo "$d"
			echo "Deleting $d"
			rm "$d"
			break
		fi
	done
done