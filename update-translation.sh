#!/bin/bash
set -e
#set -x

TRANSIFEX_USER="<TRANSIFEX_USERNAME>"
TRANSIFEX_PASSWD="<TRANSIFEX_PASSWORD>"
TRANSIFEX_API_URL="https://www.transifex.com/api/2/project/cataclysm-dda"


FTP_HOST="<WEB SITE FTP SERVER>"
FTP_USER="<FTP USERNAME>"
FTP_PASSWD="<FTP_PASSWORD>"

# Put all credentials info in this file if you want hide them.
# FTP_USER FTP_PASSWD TRANSIFEX_USER TRANSIFEX_PASSWD
#source cred.sh

# Where script will be store all files.
WORKING_DIR="<WORKING DIR>"

# This is constant values. Don't change it.
MASTER_RESOURCE="master-cataclysm-dda"
STABLE_RESOURCE="stable-cataclysm-dda"
OLD_RESOURCE="old-cataclysm-dda"

# Change it to your language.
LANG="ru"

OLD_PWD=$PWD

if [ -d "$WORKING_DIR" ]
then
    cd "$WORKING_DIR"
else
    mkdir "$WORKING_DIR"
    cd "$WORKING_DIR"
fi

# Main loop
for BRANCH in "MASTER" "STABLE" "OLD"
do
    # Magic with vars
    # Need update flag
    TO_UPDATE=false
    # Branch name in lowercase
    BR_LNAME=$(echo $BRANCH | tr '[:upper:]' '[:lower:]')
    # Transifex resource slug(internal name).
    TMP="${BRANCH}_RESOURCE"
    BR_RESOURCE=${!TMP}
    # Remote last update timestamp for branch.
    BR_REMOTE_TS=$(wget --quiet --output-document=- --user=$TRANSIFEX_USER \
    --password=$TRANSIFEX_PASSWD \
    $TRANSIFEX_API_URL/resource/$BR_RESOURCE/stats/$LANG/ | \
    grep '"last_update"' | \
    grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}')
    if [ -z "$BR_REMOTE_TS" ]
    then
        echo "'$BR_LNAME': Unable to get last update timestamp from API."
        exit 1
    else
        BR_REMOTE_TS=$(date --date="$BR_REMOTE_TS" +"%s")
    fi

    # Compare local/remote timestamps.
    BR_WORKDIR=$BR_LNAME
    if [ ! -d "$BR_WORKDIR" ]
    then
        mkdir "$BR_WORKDIR"
    fi
    if [ -f "$BR_WORKDIR/timestamp.txt" ]
    then
        BR_LOCAL_TS=$(cat "$BR_WORKDIR/timestamp.txt")
        if [ $BR_LOCAL_TS -lt $BR_REMOTE_TS ]
        then
          echo "$BR_REMOTE_TS" > $BR_WORKDIR/timestamp.txt
          TO_UPDATE=true
        fi
    else
        echo "$BR_REMOTE_TS" > $BR_WORKDIR/timestamp.txt
        TO_UPDATE=true
    fi
    if $TO_UPDATE
    then
      cd $BR_WORKDIR
      # 1. Get updated translation
      wget --quiet --output-document=${BR_LNAME}.po \
      --user=$TRANSIFEX_USER --password=$TRANSIFEX_PASSWD \
      $TRANSIFEX_API_URL/resource/$BR_RESOURCE/translation/$LANG/?file

      # 2. Compile and archive
      msgfmt -o cataclysm-dda.mo ${BR_LNAME}.po
      MO_DIR="lang/mo/$LANG/LC_MESSAGES/"
      if [ ! -d "$MO_DIR" ]
      then
        mkdir -p $MO_DIR
      fi
      cp cataclysm-dda.mo $MO_DIR
      zip -q -9 latest.zip $MO_DIR/cataclysm-dda.mo
      tar -z -c -f latest.tar.gz $MO_DIR/cataclysm-dda.mo

      # 3. Upload translation to ftp
      echo "Start uploading... $BR_LNAME updates."
      FTP_CMD="cd data/$LANG/$BR_LNAME; put latest.zip; put latest.tar.gz; \\
      put cataclysm-dda.mo; put timestamp.txt; bye"
      lftp -e "$FTP_CMD" -u $FTP_USER,$FTP_PASSWD $FTP_HOST &>/dev/null

      # 4. Clean
      rm -rf lang
      rm cataclysm-dda.mo
      rm latest.*
      rm *.po
      cd $WORKING_DIR
    fi
done
cd $OLD_PWD
