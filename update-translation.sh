#!/bin/bash
set -e
#set -x

# Transifex.com user and password
TRANSIFEX_USER=""
TRANSIFEX_PASSWD=""
# This is constant transifex.com API URL.
TRANSIFEX_API_URL="https://www.transifex.com/api/2/project/cataclysm-dda"


FTP_HOST=""
FTP_USER=""
FTP_PASSWD=""
FTP_PREFIX=""

# Put all credentials info in this file if you want hide them.
# FTP_USER FTP_PASSWD TRANSIFEX_USER TRANSIFEX_PASSWD
#source cred.sh

# Where script will be store all files.
WORKING_DIR=""

# This is constant values. Don't change it.
MASTER_RESOURCE="master-cataclysm-dda"
STABLE_RESOURCE="stable-cataclysm-dda"
OLD_RESOURCE="old-cataclysm-dda"

# Change it to your language.
LANGS="ru es_AR de it_IT es_ES"

OLD_PWD=$PWD

function check_requirements {
    check_passed=0
    for exe in "grep" "wget" "msgfmt" "tar" "zip" "lftp"
    do
        if !which $exe &>/dev/null
        then
            echo "Required executable '$exe' was not found."
            check_passed=1
        fi
    done
    for var_name in "TRANSIFEX_USER" "TRANSIFEX_PASSWD" "FTP_HOST" "FTP_USER" "FTP_PASSWD"
    do
        req_var=$var_name
        if [ -z "${!req_var}" ]
        then
            echo "Required variable '$var_name' is not set." 
            check_passed=1
        fi
    done
    return $check_passed
}

if [ -d "$WORKING_DIR" ]
then
    cd "$WORKING_DIR"
else
    if [ -z "$WORKING_DIR" ]
    then
        echo "You need to specify full path of working directory."
        echo "Working directory value is stored in \$WORKINGDIR variable."
        exit 1
    fi
    echo "Initial run. Check parameters..."
    check_requirements
    mkdir "$WORKING_DIR"
    cd "$WORKING_DIR"
fi

# Main loop
for LL in $LANGS
do
    if [ ! -d "$WORKING_DIR/$LL" ]
    then
        mkdir "$WORKING_DIR/$LL"
    fi
    cd "$WORKING_DIR/$LL"
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
        $TRANSIFEX_API_URL/resource/$BR_RESOURCE/stats/$LL/ | \
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
          $TRANSIFEX_API_URL/resource/$BR_RESOURCE/translation/$LL/?file

          # 2. Compile and archive
          msgfmt -o cataclysm-dda.mo ${BR_LNAME}.po
          MO_DIR="lang/mo/$LL/LC_MESSAGES/"
          if [ ! -d "$MO_DIR" ]
          then
            mkdir -p $MO_DIR
          fi
          cp cataclysm-dda.mo $MO_DIR
          zip -q -9 latest.zip $MO_DIR/cataclysm-dda.mo
          tar -z -c -f latest.tar.gz $MO_DIR/cataclysm-dda.mo

          # 3. Upload translation to ftp
          echo "Start uploading... $BR_LNAME updates."
          FTP_CMD="cd $FTP_PREFIX/$LL/$BR_LNAME; put latest.zip; put latest.tar.gz; \\
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
done
cd $OLD_PWD
