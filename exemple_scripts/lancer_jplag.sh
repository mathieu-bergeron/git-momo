tag=$1


if [ "$tag" = "" ]; then
    echo usage: $0 TAG
    exit
fi

#javacmd=/etc/alternatives/java
javacmd=/usr/lib/jvm/java-11-openjdk-amd64/bin/java
jplagjar=jplag-2.12.1-SNAPSHOT-jar-with-dependencies.jar 
outdir=atelier$tag
collect_pattern="[Aa]telier$tag"
exclude_pattern="MonAtelier$tag.*java$"

./launch_jplag.py -o $outdir -p "$collect_pattern" -e "$exclude_pattern" -j $javacmd -jplag $jplagjar -b firefox
