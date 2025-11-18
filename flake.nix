{
  description = "A devshell flake with latex, python, and assignment profiles";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
    fhsEnvironment = {
      LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
        pkgs.stdenv.cc.cc.lib
        pkgs.libz
      ];
    };
    python = pkgs.mkShell {
      packages = [
        pkgs.python3
        pkgs.python3Packages.pip
        pkgs.imagemagick
        pkgs.python3Packages.virtualenv
        pkgs.zstd
        pkgs.ghostscript
      ];
      shellHook = ''
        if [ ! -d ".venv" ]; then
          virtualenv .venv
        fi
        source .venv/bin/activate
        if [ -f "requirements.txt" ]; then
          pip install -r requirements.txt
        fi
      '';
      env = fhsEnvironment;
    };
    latex = pkgs.mkShell {
      packages = [
        (pkgs.texliveSmall.withPackages (
          ps:
            with ps; [
              amsfonts
              appendix
              biblatex
              csquotes
              doublestroke
              enumitem
              esint
              framed
              pdfcol
              physics
              rsfs
              tikzfill
              tcolorbox
              titlesec
            ]
        ))
      ];
    };
  in {
    devShells.x86_64-linux = {
      python = python;
      latex = latex;
      default = pkgs.mkShell {
        inputsFrom = [
          python
          latex
        ];
        env = fhsEnvironment;
      };
    };
  };
}
