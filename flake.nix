{
  description = "Development Shell for running Solstice in a reproducible environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = {...} @ inputs: let
    inherit (inputs.nixpkgs) lib;

    systems = ["x86_64-linux" "aarch64-linux"];
    eachSystem = lib.genAttrs systems;

    # Done very similarly to https://github.com/hyprwm/Hyprland/blob/main/flake.nix
    pkgsFor = eachSystem (system: inputs.nixpkgs.legacyPackages.${system});
  in {
    formatter = eachSystem (system: inputs.nixpkgs.legacyPackages.${system}.alejandra);

    devShells = eachSystem (system: let
      pkgs = pkgsFor.${system};
    in {
      default = pkgs.mkShellNoCC {
        nativeBuildInputs = let
          requirements = ps:
            with ps; [
              blinker
              click
              itsdangerous
              jinja2
              markupsafe
              numpy
              opencv4
              pillow
              # setuptools
              werkzeug
              # wheel
            ];
        in [(pkgs.python312.withPackages requirements)];
      };
    });
  };
}
