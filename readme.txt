                    Tema 2, SPRC
            Salcie Ioan-Cristian, 341C1

In rezolvarea temei am decis sa folosesc limbajul Python impreuna cu
framework-ul "Flask" si baza de date "MongoDB" folosind driver-ul de
python "pymongo" pentru accesarea bazei de date.

Pentru construirea temei (baza de date + REST API) se va rula scriptul:
./rebuild_restapi.sh

Pentru aplicarea schimbarilor in REST API pe parcusul rezolvarii temei
am creat un script "update_restapi_src.sh". Asadar cat timp am dezvoltat
tema am avut comentata linia "CMD ["python3", "main.py"]" din
    "rest_api/dockerfile"
pentru a nu mai rula automat fisierul cu rezolvarea temei si necomentata
linia "tty: true" din
    "rest_api/docker-compose.yml"
pentru a tine docker-ul in starea "UP" ca sa pot intra in el si sa rulez
manual comanda "python3 main.py".

Comenzi utile:
    // pentru rularea unui docker-compose
    sudo docker-compose -f docker-compose.yml up -d

    // pentru oprirea unui docker-compose
    sudo docker-compose down

    // pentru a sterge configuratia
    sudo docker-compose rm

    // pentru a vedea ce porturi sunt folosite:
    sudo lsof -i -P -n | grep LISTEN

    // pentru a vedea retelele docker
    docker network ls

    // pentru a vedea volumele docker
    docker volume ls

    // pentru a intra in container
    sudo docker exec -it rest_api_sprc_hw2 /bin/bash

    // pentru a copia in container
    docker cp <sursa> <destinatie>

Bibliografie:
    https://www.bmc.com/blogs/mongodb-docker-container/
    https://kb.objectrocket.com/mongo-db/use-docker-and-python-for-a-mongodb-application-1046
    https://www.tutorialworks.com/container-networking/
    https://www.guru99.com/working-mongodb-indexes.html
    https://stackoverflow.com/questions/32490629/getting-todays-date-in-yyyy-mm-dd-in-python
    https://stackoverflow.com/questions/20365854/comparing-two-date-strings-in-python
    https://codefresh.io/docker-tutorial/not-ignore-dockerignore-2/
