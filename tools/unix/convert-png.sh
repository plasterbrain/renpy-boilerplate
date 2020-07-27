find ./ -type f -name '*.png' -exec cwebp -lossless -z 9 {} -o "{}.webp" _ {} \;
mmv ";*.png.webp" "#2.webp";
read -p "Press enter when you're ready to delete old png images."
rm -r *.png
