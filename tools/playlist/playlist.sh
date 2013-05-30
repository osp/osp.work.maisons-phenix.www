dir=$(pwd)
cd ../../phenix
rdfproc -c aa query sparql - "PREFIX aa:<http://activearchives.org/terms/> select ?s where { ?s aa:${1} \"${2}\"@fr }" | tr "<" "\n" | tr ">" "\n" | grep http > "${dir}/play.list" && mplayer -playlist "${dir}/play.list"
