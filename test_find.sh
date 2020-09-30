pattern=".*"

if [ "$1" != "" ]; then
    pattern="$1"
fi

./find_repos.py -i test_data/after_clone.json  "$pattern"
