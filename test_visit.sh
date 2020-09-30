pattern=".*"

if [ "$1" != "" ]; then
    pattern="$1"
fi

./visit_repos.py -i test_data/after_clone.json  "$pattern"
