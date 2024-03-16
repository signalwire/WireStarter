#!/bin/sh
git pull
export WORKDIR=/workdir/
docker pull briankwest/wirestarter
docker kill wirestarter
#docker run -it -d --rm --name wirestarter briankwest/wirestarter
#docker run -it -d --rm --name wirestarter --volume "${WORKDIR}:/workdir/" briankwest/wirestarter
#docker run -it -d --name wirestarter --env-file /workdir/.env --volume "${WORKDIR}:/workdir" --volume opt:/opt briankwest/wirestarter /start_services.sh || echo "up"
docker run -it -d --rm --name wirestarter --env-file /workdir/.env --volume "${WORKDIR}:/workdir" --volume opt:/opt briankwest/wirestarter /start_services.sh || echo "up"
docker exec -ti wirestarter bash
