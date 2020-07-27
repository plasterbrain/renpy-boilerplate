find ./ -type f -name '*.jpg' -exec cwebp {} -o "{}.webp" _ {} \;
mmv ";*.jpg.webp" "#2.webp";
read -p "Press enter when you're ready to delete old jpg images."
rm -r *.jpg
