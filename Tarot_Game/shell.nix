{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
      tkinter
      pillow
    ]))
  ];
}

# nix-shell --run "python main.py"