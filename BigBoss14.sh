#!/bin/bash

clear

echo -e "\nNote:- Use Network activity option in DevTools to grab Contestant Id and Name\n"

read -p 'Enter the name of Contestant:- ' name
read -p 'Enter Contestant Id:- ' conId

for i in $(seq 1 20000)
do
    if [ $i -eq 1 ]
    then
        echo -e "\n[+] Preparing for 1st Vote [+]\n"
    elif [ $i -eq 2 ]
    then
        echo -e "[+] Preparing for 2nd Vote [+]\n"
    elif [ $i -eq 3 ]
    then
        echo -e "[+] Preparing for 3rd Vote [+]\n"
    else
        echo -e "\n\n[+] Preparing for ${i}th Vote [+]"
        echo -e "---------------------------------"
    fi
    echo -e "\n[+] Grabbing JWT Access Token of XXXXXXXX@gmail.com\n"


    mail="XXXXXXXX@gmail.com"

    #To login:-
    login=$(curl -s 'https://us-central1-vootdev-stg.cloudfunctions.net/usersV3/v3/login' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Content-Type: application/json;charset=utf-8' -H 'Origin: https://voting.voot.com' -H 'Connection: keep-alive' -H 'Referer: https://voting.voot.com/vote/ec324230-02f2-11eb-bf8c-d128fef771cc?&platform=web' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'TE: Trailers' --data-raw '{"type":"traditional","deviceId":"Windows NT 10.0","deviceBrand":"PC/MAC","data":{"email":"'"$mail"'","password":"XXXXXXXXXXXXX"}}')




    #Extract Access Token:-
    AccessToken=$(echo "$login" | jq -r '.data.authToken.accessToken')
    echo -e "==> AccessToken:-\n ----------------- \n $AccessToken\n"

    #Extract User Id:-
    UserId=$(echo "$login" | jq -r '.data.uId')
    echo -e "==> User ID:-\n ------------- \n $UserId\n\n"

    echo -e "[+] Generating JWT Authentication Token for XXXXXXXX@gmail.com account"

    #To query for Auth Token:-
    getAuth=$(curl -sL --request GET -H "Referer: https://voting.voot.com/vote/ec324230-02f2-11eb-bf8c-d128fef771cc?&platform=web" -H "Deviceinfo: Windows NT 10.0" -H "Lastloginprovider: Traditional" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0" -H "Accept: application/json, text/plain, */*" -H "Origin: https://voting.voot.com" -H "Uid: $UserId" -H "Accesstoken: $AccessToken" -H "Buildnumber: v0" https://us-central1-vootdev.cloudfunctions.net/usersV3/v3/getAuthKey)


    #Extract Auth Token:-
    authToken=$(echo "$getAuth" | grep "accessToken" | cut -d':' -f 2 | sed 's/"//g' | sed 's/}//g')

    echo -e "==> JWT Auth Token:- \n ---------------------"
    echo "$authToken"

    echo -e "\n"

    echo -e "[+] Verifying JWT Token \n --------------------"

    #To verify JWT:-
    verifyJWT=$(curl -sL --request POST --data '{"token":"'$authToken'"}' -H "Accept-Encoding: gzip, deflate, br" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0" -H "Origin: https://voting.voot.com" -H "Content-Type: application/json" https://voting-api.voot.com/v1/verifyjwttoken)

    #Extract UID:-
    JWT=$(echo "$verifyJWT" | jq -r '.UID')

    echo -e "$verifyJWT\n"

    #Verifying JWT Token:-
    if [ "$UserId" == "$JWT" ]
    then
        echo "+---------------------------------+"
        echo -e "| JWT Token verified successfully |"
        echo "+---------------------------------+"
    else
        echo -e "Verification Failed"
    fi

    echo "*** Doing Voting, Please Wait ***"

    curl -sL 'https://voting-api.voot.com/v1/addvote' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Content-Type: application/json' -H 'Origin: https://voting.voot.com' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' --data-raw '{"showId":"ec324230-02f2-11eb-bf8c-d128fef771cc","showName":"Bigg Boss 14","categoryId":"","categoryName":"","contestantId":"'"$conId"'","contestantName":"'"$name"'","cycleId":"e22aea10-1ded-11eb-a795-5100ad300b39","userId":"'"$UserId"'","userName":"","userEmail":"'"$mail"'","region":"in","ip":"202.142.67.82","loginProvider":"Traditional"}'

    echo -e "\n-----------------------------------------------------X----------------------------------------------\n"


done

