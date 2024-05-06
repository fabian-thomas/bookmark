{ stdenv, python3, makeWrapper, imagemagick_light }:

stdenv.mkDerivation {
  pname = "bookmark";
  version = "1.0";

  src = ./.;

  buildInputs = [
    (python3.withPackages (p: with p; [ tldextract favicon requests ]))
    makeWrapper
    imagemagick_light
  ];

  DESTDIR=placeholder "out";

  postFixup = ''
    wrapProgram $out/bin/rofi-bookmark-download.py --set BOOKMARK_TOOL $out/bin/bookmark --set CONVERT_TOOL ${imagemagick_light}/bin/convert
  '';
}
