{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
      tkinter
      pillow
      python-dotenv
      requests
    ]))
  ];
}

# nix-shell --run "python main.py"