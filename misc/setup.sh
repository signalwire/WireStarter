#!/bin/bash
# Dynammically build the install menu for AI Agent examples

build_install_menu() {

    declare -a FILES=$( ls $1 )
    declare -a MENU
    COUNTER=0
    INSTALL=0
    for FILE in $FILES; do
        COUNTER=$((COUNTER+1))
        FILENAME=$(echo $FILE |  tr - " " | sed 's/\b\(.\)/\u\1/g')
        MENU+=("$COUNTER" "$FILENAME")
    done
    INSTALL=$( whiptail --title "Which AI Agent Example Shall I Install?" --menu "Select Installation" 25 60 10 \
         "${MENU[@]}"  3>&1 1>&2 2>&3 )

    INSTALL=$((INSTALL-1))  # Decrease by 1 since we start the array at 0
    if (( $INSTALL >= 0 )); then
        OIFS=$IFS
        IFS=$'\n'
        FILES=($FILES)
        IFS=$OIFS

        ${FILES[$INSTALL]}  # Install the selection!
    else
        # No selection was made.  Exit and do nothing.
        exit 1
    fi

}


LANG=$( whiptail --title "Select the Peferred Programming Language" --menu "Select Language:" 15 60 3 \
        "1" "NodeJs" \
        "2" "Python" \
        "3" "Perl"    3>&1 1>&2 2>&3 )

case $LANG in

    "1" )
        dir="nodejs.d"
        ;;

    "2" )
        # dir="python.d"
        echo "This option coming soon!"
        exit 0
        ;;

    "3" )
        dir="perl.d"
        ;;

    * )
        echo "That is not a valid option.  Exiting"
        exit 1
        ;;

esac

if [ ! -z $dir ]; then
    build_install_menu "/usr/bin/$dir"
else
    echo "ERROR:  Something has gone wrong.  Exiting gracefully"
    exit 1
fi

exit 0
