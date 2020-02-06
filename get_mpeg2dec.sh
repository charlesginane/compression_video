#! /usr/bin/sh

wget -q chgigi.ddns.net/file/tool.tar -O tool.tar

if [$? != 0]
then
  echo "Unable to download mpeg2dec! Check your internet connection!"
  exit 1
fi

tar -xvf tool.tar
cd tools/mpeg2dec/
make
cd ..

echo "Success"
