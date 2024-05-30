{
  description = "Development Shell for running Solstice in a reproducible environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = {...} @ inputs: let
    inherit (inputs.nixpkgs) lib;

    systems = ["x86_64-linux" "aarch64-linux"];
    eachSystem = lib.genAttrs systems;

    pkgsFor = eachSystem (system:
      import inputs.nixpkgs {
        inherit system;

        overlays = [
          (final: prev: {
            opencv4 = prev.opencv4.override {
              enableGtk3 = true;
            };
          })
        ];
      });
  in {
    formatter = eachSystem (system: inputs.nixpkgs.legacyPackages.${system}.alejandra);

    devShells = eachSystem (system: let
      pkgs = pkgsFor.${system};
      pythonWithPackages = pkgs.python312.withPackages (ps:
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
        ]);
    in {
      default = pkgs.mkShell {
        packages = [pythonWithPackages];
      };
    });
  };
}
