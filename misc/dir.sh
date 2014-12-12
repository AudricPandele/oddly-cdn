#Scaffolding the whole project structure, mainly for media directory

read -p "Type the CDN path (without trailing slash plz): " cdn_path

if find $cdn_path -name "manage.py"
then
    echo " Artist covers directory"
    mkdir -p $cdn_path/media/artist/covers
    echo "Artist thumbs directory"
    mkdir -p $cdn_path/media/artist/thumbs
    echo "Item pdf origin directory"
    mkdir -p $cdn_path/media/items/pdf/original
    echo "Item covers directory"
    mkdir -p $cdn_path/media/items/covers
    echo "Item processed directory"
    mkdir -p $cdn_path/media/items/processed
    
    echo "All done"
else
    echo "I can't found manage.py, make sure the path is okay"
    read -p "Type the CDN path" cdn_path
    if find $cdn_path -name "manage.py"
    then
        echo " Artist covers directory"
        mkdir -p $cdn_path/media/artist/covers
        echo "Artist thumbs directory"
        mkdir -p $cdn_path/media/artist/thumbs
        echo "Item pdf origin directory"
        mkdir -p $cdn_path/media/items/pdf/original
        echo "Item covers directory"
        mkdir -p $cdn_path/media/items/covers
        echo "Item processed directory"
        mkdir -p $cdn_path/media/items/processed
        echo "All done"
    else
        echo "You are obviously derping"
    fi

fi
