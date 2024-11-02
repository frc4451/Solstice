{
  description = "Development Shell for running Solstice in a reproducible environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {...} @ inputs: let
    inherit (inputs.nixpkgs) lib;

    systems = ["x86_64-linux" "aarch64-linux"];
    eachSystem = lib.genAttrs systems;

    pkgsFor = eachSystem (system:
      import inputs.nixpkgs {
        inherit system;

        overlays = [
          (final: prev: {
            python3 = prev.python3.override {
              packageOverrides = self: super: {
                mjpeg-streamer = self.callPackage nix/pkgs/mjpeg-streamer {};
                pyntcore = self.callPackage nix/pkgs/pyntcore {};
                robotpy-wpinet = self.callPackage nix/pkgs/robotpy-wpinet {};
                robotpy-wpiutil = self.callPackage nix/pkgs/robotpy-wpiutil {};
              };
            };
          })
        ];
      });
  in {
    formatter = eachSystem (system: inputs.nixpkgs.legacyPackages.${system}.alejandra);

    devShells = eachSystem (system: let
      pkgs = pkgsFor.${system};
      pythonWithPackages = pkgs.python3.withPackages (ps:
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

          mjpeg-streamer
          pyntcore
        ]);

      # https://wiki.nixos.org/wiki/GStreamer
      gstreamerPackages = with pkgs; [
        # Video/Audio data composition framework tools like "gst-inspect", "gst-launch" ...
        gst_all_1.gstreamer
        # Common plugins like "filesrc" to combine within e.g. gst-launch
        gst_all_1.gst-plugins-base
        # Specialized plugins separated by quality
        gst_all_1.gst-plugins-good
        # gst_all_1.gst-plugins-bad
        # gst_all_1.gst-plugins-ugly
        # Plugins to reuse ffmpeg to play almost every video format
        # gst_all_1.gst-libav
        # Support the Video Audio (Hardware) Acceleration API
        gst_all_1.gst-vaapi
        # ...
      ];
    in {
      default = pkgs.mkShell {
        packages =
          [pythonWithPackages]
          ++ gstreamerPackages
          ++ (with pkgs; [
            black
            isort
          ]);
        shellHook = ''
          export GST_V4L2_USE_LIBV4L2=1
        '';
      };
    });
  };
}
