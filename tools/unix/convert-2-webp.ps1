$images = @(Get-ChildItem -Path * -Recurse | where {$_.extension -in ".png",".jpg",".jpeg"})

if ($Files.length -eq 0) {
	Write-Host "No images found. Press any key to continue..."
	$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} else {
	foreach ($img in $images) {
		$outputName = $img.DirectoryName + "\" + $img.BaseName + ".webp"
        if ($img.extension -eq ".png" ) {
		    cwebp -lossless -z 9 $img.FullName -o $outputName
        } else {
            cwebp $img.FullName -o $outputName
        }
	}

	Remove-Item -Path * -Recurse -Include ("*.png","*.jpg","*.jpeg") -Confirm
}