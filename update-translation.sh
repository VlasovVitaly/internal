#!/bin/bash
set -e
#set -x

TRANSIFEX_USER="<TRANSIFEX_USERNAME>"
TRANSIFEX_PASSWD="<TRANSIFEX_PASSWORD>"
TRANSIFEX_API_URL="https://www.transifex.com/api/2/project/cataclysm-dda"


FTP_HOST="<WEB SITE FTP SERVER>"
FTP_USER="<FTP USERNAME>"
FTP_PASSWD="<FTP_PASSWORD>"

source cred.sh

LOCAL_DIR_ROOT=$PWD
WORKING_DIR="$LOCAL_DIR_ROOT"

MASTER_RESOURCE="master-cataclysm-dda"
STABLE_RESOURCE="stable-cataclysm-dda"
OLD_RESOURCE="old-cataclysm-dda"

STABLE_TS_FILE="stable-timestamp.txt"
MASTER_TS_FILE="master-timestamp.txt"
OLD_TS_FILE="old-timestamp.txt"

LANG="ru" # Change it to yout language.

if [ -d "$WORKING_DIR" ]
then
    cd "$WORKING_DIR"
else
    mkdir "$WORKING_DIR"
    cd "$WORKING_DIR"
fi

# Main timestamp loop
for BRANCH in "MASTER" "STABLE" "OLD"
do
    # Magic with vars
    TO_UPDATE=false
    BR_LNAME=$(echo $BRANCH | tr '[:upper:]' '[:lower:]')
    TMP="L_TS_$BRANCH"
    BR_LOCAL_TS=${!TMP}
    TMP="${BRANCH}_RESOURCE"
    BR_RESOURCE=${!TMP}
    TMP="${BRANCH}_TS_FILE"
    BR_TS_FILE=${!TMP}
    echo "DEBUG: BR RESOURCE: $BR_RESOURCE"
    # Get remote last-update timestamp
    BR_REMOTE_TS=$(wget --quiet --output-document=- --user=$TRANSIFEX_USER \
    --password=$TRANSIFEX_PASSWD \
    $TRANSIFEX_API_URL/resource/$BR_RESOURCE/stats/$LANG/ | \
    grep '"last_update"' | \
    grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}')
    echo "DEBUG: BR REM TS: $BR_REMOTE_TS"
    if [ -z "$BR_REMOTE_TS" ]
    then
        echo "Can't get last update info for Master branch"
        exit 1
    else
        BR_REMOTE_TS=$(date --date="$BR_REMOTE_TS" +"%s")
    fi
    echo "DEBUG: BR REM TS: $BR_REMOTE_TS"
    # Check local timestamp for branch
    BR_WORKDIR=$BR_LNAME
    if [ -d "./$BR_WORKDIR" ]
    then
        echo "Branch $BR_WORKDIR EXIST"
    else
        echo "BR WORK $BR_WORKDIR DIR IS empty"
        mkdir "./$BR_WORKDIR"
    fi
    if [ -f "$BR_WORKDIR/timestamp.txt" ]
    then
        echo "Branch TS file exist. Checking value."
        BR_LOCAL_TS=$(cat "$BR_WORKDIR/timestamp.txt")
        echo "DEBUG: BR LOCAL_TS: $BR_LOCAL_TS"
        if [ $BR_LOCAL_TS -lt $BR_REMOTE_TS ]
        then
          TO_UPDATE=true
          echo "Need update to $BR_LNAME branch"
        else
          echo "Branch '$BR_LNAME' don't need update"
        fi
    else
        echo "$BR_REMOTE_TS" > $BR_WORKDIR/timestamp.txt
        TO_UPDATE=true
        echo "Branch TS file does not exist."
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
      if [ -d "$MO_DIR" ]
      then
        cp cataclysm-dda.mo $MO_DIR
      else
        mkdir -p $MO_DIR
        cp cataclysm-dda.mo $MO_DIR
      fi
      zip -q -9 latest.zip $MO_DIR/cataclysm-dda.mo
      tar -z -c -f latest.tar.gz $MO_DIR/cataclysm-dda.mo

      # 3. Upload translation to ftp
      echo "Start uploading... $BR_LNAME"
      FTP_CMD="cd data/$LANG/$BR_LNAME; put latest.zip; put latest.tar.gz; \\
      put cataclysm-dda.mo; put timestamp.txt; bye"
      lftp -e "$FTP_CMD" -u $FTP_USER,$FTP_PASSWD $FTP_HOST 

      # 4. Clean
      rm -rf lang
      rm cataclysm-dda.mo
      rm latest.*
      rm *.po
      cd $WORKING_DIR
    fi
done # End of main loop

if [ -z "$TO_UPDATE" ]
then
    echo "Nothing to update. Exit."
    exit 0
fi

for BRANCH in $TO_UPDATE
do
    if [ $BRANCH = "master" ]
    then
        # Stage 1 download translation
        echo "DEBUG: master need update!!!!"
        wget --quiet --output-document=master.po \
        --user=$TRANSIFEX_USER --password=$TRANSIFEX_PASSWD \
        $TRANSIFEX_API_URL/resource/$MASTER_RESOURCE/translation/$LANG_LL/?file
        # Stage 2 Compile and archive
        msgmft -o cataclysm-dda.mo master.po
        if [ ! -d lang/mo/$LANG_LL/LC_MESSAGES ]; then
            mkdir -p lang/mo/$LANG_LL/LC_MESSAGES
        fi
        mv cataclysm-dda.mo lang/mo/$LANG_LL/LC_MESSAGES/
        tar -z -c -f latest.tar.gz
        zip -q -9 latest.zip

        # Stage 3 send to server
        FTP_CMD="cd data/$LANG_LL/$BRANCH; put lattest.zip; put master.tar.gz; \\
        put cataclysm-dda.mo; put master-timestamp.txt -o timestamp.txt; bye"
        lftp -e "$FTP_CMD" -u $FTP_URES,$FTP_PASSWD $FTP_HOST &>/dev/null

        # Stage 4 clean
    fi
    if [ $BRANCH = "stable" ]
    then
        echo "DEBUG: stable need update!!!!"
    fi
done
